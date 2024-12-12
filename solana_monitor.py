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

def get_signature_info(client, signature):
    """Get detailed transaction information for a signature"""
    try:
        tx_info = client.get_transaction(signature)
        if tx_info is None or 'result' not in tx_info:
            return None
        return tx_info['result']
    except Exception as e:
        print(f"Error fetching transaction info: {e}")
        return None

def display_transaction(console, tx_info):
    """Display transaction information in a beautiful format"""
    if not tx_info:
        return

    # Create a table for transaction details
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="green")

    # Extract basic transaction information
    block_time = datetime.fromtimestamp(tx_info['blockTime'])
    fee = format_lamports_to_sol(tx_info['meta']['fee'])
    status = "Success" if tx_info['meta']['status']['Ok'] is None else "Failed"

    # Add rows to the table
    table.add_row("Timestamp", str(block_time))
    table.add_row("Status", status)
    table.add_row("Fee (SOL)", f"{fee:.9f}")

    # Get pre and post token balances
    pre_balances = tx_info['meta']['preBalances']
    post_balances = tx_info['meta']['postBalances']

    if pre_balances and post_balances:
        balance_change = format_lamports_to_sol(post_balances[0] - pre_balances[0])
        table.add_row("Balance Change (SOL)", f"{balance_change:+.9f}")

    # Display the table in a panel
    console.print(Panel(table, title=f"[bold blue]Transaction: {tx_info['transaction']['signatures'][0][:20]}..."))
    console.print()

def main():
    # Initialize Rich console for beautiful output
    console = Console()

    # Connect to Solana mainnet
    client = Client("https://api.mainnet-beta.solana.com")

    console.print("[bold green]🔍 Monitoring Solana transactions...[/bold green]")

    try:
        # Convert string address to Pubkey
        address = Pubkey.from_string("9xQeWvG816bUx9EPjHmaT23yvVM2ZWbrrpZb9PusVFin")

        # Get recent signatures
        while True:
            signatures = client.get_signatures_for_address(address)

            for sig_info in list(signatures)[:5]:
                tx_info = get_signature_info(client, sig_info.signature)
                if tx_info:
                    display_transaction(console, tx_info)

            time.sleep(5)
            console.print("[bold yellow]Updating...[/bold yellow]")

    except KeyboardInterrupt:
        console.print("[bold red]Monitoring stopped.[/bold red]")
    except Exception as e:
        console.print(f"[bold red]An error occurred: {e}[/bold red]")

if __name__ == "__main__":
    main()