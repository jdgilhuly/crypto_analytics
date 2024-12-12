from solana.rpc.api import Client
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from datetime import datetime
import time
from solders.pubkey import Pubkey

def format_lamports_to_sol(lamports):
    """Convert lamports to SOL"""
    return lamports / 1_000_000_000

def get_signature_info(client, signature, console):
    """Get detailed transaction information for a signature"""
    try:
        tx_info = client.get_transaction(
            signature,
            max_supported_transaction_version=0
        )
        if tx_info is None:
            console.print(f"[yellow]Transaction {str(signature)[:20]}... not found (might be too old)[/yellow]")
            return None
        return tx_info
    except Exception as e:
        console.print(f"[red]Error fetching transaction {str(signature)[:20]}...: {str(e)}[/red]")
        return None

def display_transaction(console, tx_info):
    """Display transaction information in a beautiful format"""
    if not tx_info:
        return

    # Create a table for transaction details
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="green")

    # Extract basic transaction information from the correct properties
    block_time = datetime.fromtimestamp(tx_info.value.block_time)
    fee = format_lamports_to_sol(tx_info.value.transaction.meta.fee)

    # Check if the transaction was successful
    status = "Success" if tx_info.value.transaction.meta.err is None else "Failed"

    # Add rows to the table
    table.add_row("Timestamp", str(block_time))
    table.add_row("Status", status)
    table.add_row("Fee (SOL)", f"{fee:.9f}")

    # Get pre and post token balances
    pre_balances = tx_info.value.transaction.meta.pre_balances
    post_balances = tx_info.value.transaction.meta.post_balances

    if pre_balances and post_balances:
        balance_change = format_lamports_to_sol(post_balances[0] - pre_balances[0])
        table.add_row("Balance Change (SOL)", f"{balance_change:+.9f}")

    # Convert signature to string before slicing
    signature = str(tx_info.value.transaction.transaction.signatures[0])
    console.print(Panel(table, title=f"[bold blue]Transaction: {signature[:20]}..."))
    console.print()

def main():
    console = Console()
    client = Client("https://api.mainnet-beta.solana.com")
    console.print("[bold green]🔍 Monitoring Solana transactions...[/bold green]")

    try:
        address = Pubkey.from_string("9xQeWvG816bUx9EPjHmaT23yvVM2ZWbrrpZb9PusVFin")

        while True:
            signatures = client.get_signatures_for_address(address).value

            if not signatures:
                console.print("[yellow]No recent transactions found[/yellow]")
            else:
                console.print(f"[green]Found {len(signatures)} recent transactions[/green]")

            for sig_info in signatures[:5]:
                tx_info = get_signature_info(client, sig_info.signature, console)
                if tx_info:
                    display_transaction(console, tx_info)

            time.sleep(5)
            console.print("\n[bold yellow]Updating...[/bold yellow]")

    except KeyboardInterrupt:
        console.print("[bold red]Monitoring stopped.[/bold red]")
    except Exception as e:
        console.print(f"[bold red]An error occurred: {e}[/bold red]")

if __name__ == "__main__":
    main()