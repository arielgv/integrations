from rich.console import Console
from rich.table import Table
from perps.core.event_loop import EventLoop
from perps.core.timer_feed import TimerFeed, TimerListener
from perps.core.exchange_state_factory import ExchangeStatesFactory


class Strat(TimerListener):

    def __init__(self, exchange_states):
        self.exchange_states = exchange_states
        self.funding_rates = {}

    def on_timer(self):
        for key in self.exchange_states:
            fr_df = self.exchange_states[key].fr_df
            for idx in fr_df.index:
                ticker = fr_df.loc[idx, "ticker"]
                if ticker not in self.funding_rates:
                    self.funding_rates[ticker] = {}
                fr = fr_df.loc[idx, "fr"]
                self.funding_rates[ticker][key] = fr
        self.find_arbs()

    def find_arbs(self):
        arbs = []
        for ticker in self.funding_rates:
            if len(self.funding_rates[ticker]) >= 2:
                rates = sorted(self.funding_rates[ticker].items(), key=lambda x: x[1])[
                    ::-1
                ]
                fr_diff = 100 * (rates[0][1] - rates[-1][1])
                arbs.append(
                    {
                        "ticker": ticker,
                        "exch1": rates[0][0],
                        "exch2": rates[-1][0],
                        "fr_diff_1h": fr_diff,
                        "fr_diff_1y": fr_diff * 24 * 365,
                        "fr1": 100 * rates[0][1],
                        "fr2": 100 * rates[-1][1],
                    }
                )
        arbs = sorted(arbs, key=lambda x: abs(x["fr_diff_1y"]))[::-1]
        self.print_arbs(arbs)

    def print_arbs(self, arbs):
        table = Table(title="Arbs")
        table.add_column("Ticker")
        table.add_column("Short On")
        table.add_column("Long On")
        table.add_column("FR Diff 1h")
        table.add_column("FR Diff 1y")
        table.add_column("FR Short")
        table.add_column("FR Long")
        for arb in arbs:
            table.add_row(
                arb["ticker"],
                arb["exch1"],
                arb["exch2"],
                f"{arb['fr_diff_1h']:.4f}%",
                f"{arb['fr_diff_1y']:.2f}%",
                f"{arb['fr1']:.4f}%",
                f"{arb['fr2']:.4f}%",
            )

        console = Console()
        console.print(table)


if __name__ == "__main__":
    import sys
    import dotenv
    dotenv.load_dotenv()
    try:
        exchanges = ["rabbitx", "hyperliquid", "dydx"]
        factory = ExchangeStatesFactory()
        event_loop = EventLoop()
        exchange_states = factory.build_exchange_states(exchanges, event_loop)
        strat = Strat(exchange_states)
        # default every ten seconds:
        feed = TimerFeed(freq_ms=10 * 1000)
        feed.add_listener(strat)
        event_loop.add_feed(feed)
        event_loop.run()
    except KeyboardInterrupt:
        print("\nExiting on ctrl-c")
        sys.exit(0)
