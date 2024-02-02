import ccxt.pro
from asyncio import gather, run

# Initialisation des dictionnaires pour stocker les prix d'offre et de demande pour chaque paire sur chaque exchange
bid_prices = {}
ask_prices = {}

async def symbol_loop(exchange, symbol, profit_threshold):
    while True:
        try:
            orderbook = await exchange.watch_order_book(symbol)
            now = exchange.milliseconds()
            bid_price = orderbook["bids"][0][0] if orderbook["bids"] else None
            ask_price = orderbook["asks"][0][0] if orderbook["asks"] else None

            bid_prices[(exchange.id, symbol)] = bid_price
            ask_prices[(exchange.id, symbol)] = ask_price

            filtered_bids = {k: v for k, v in bid_prices.items() if k[1] == symbol}
            filtered_asks = {k: v for k, v in ask_prices.items() if k[1] == symbol}
            if not filtered_bids or not filtered_asks:
                continue

            min_ask_ex, min_ask_price = min(filtered_asks.items(), key=lambda x: x[1])
            max_bid_ex, max_bid_price = max(filtered_bids.items(), key=lambda x: x[1])

            best_diff_pct = ((max_bid_price - min_ask_price) / min_ask_price) * 100 if min_ask_price else 0

            # Filtrer les résultats en fonction du pourcentage de profit
            if best_diff_pct >= profit_threshold:
                profit_sign = "+" if best_diff_pct > 0 else ""
                print(f"{symbol} | {min_ask_ex[0]} | {max_bid_ex[0]} | {profit_sign}{round(best_diff_pct, 2)} % | {min_ask_price}$ | {max_bid_price}$ | {max_bid_price - min_ask_price}$")
        except Exception as e:
            print(str(exchange) + " -> " + str(e))
            break

async def exchange_loop(exchange_id, symbols, profit_threshold):
    exchange = getattr(ccxt.pro, exchange_id)()
    loops = [symbol_loop(exchange, symbol, profit_threshold) for symbol in symbols]
    await gather(*loops)
    await exchange.close()

async def main():
    profit_threshold = 0.3
    exchanges = {
        # "okx": ["ETH/USDT", "BNB/USDT", "SOL/USDT", "ADA/USDT", "AVAX/USDT", "DOGE/USDT", "TRX/USDT", "LINK/USDT", "DOT/USDT", "MATIC/USDT", "TON/USDT", "DAI/USDT"],
        # "kucoin": ["ETH/USDT", "BNB/USDT", "SOL/USDT", "ADA/USDT", "AVAX/USDT", "DOGE/USDT", "TRX/USDT", "LINK/USDT", "DOT/USDT", "MATIC/USDT", "TON/USDT", "DAI/USDT"],
        # "binance": ["ETH/USDT", "BNB/USDT", "SOL/USDT", "ADA/USDT", "AVAX/USDT", "DOGE/USDT", "TRX/USDT", "LINK/USDT", "DOT/USDT", "MATIC/USDT", "TON/USDT", "DAI/USDT"],
        # "htx": ["ETH/USD", "BNB/USD", "SOL/USD", "ADA/USDT", "AVAX/USDT", "DOGE/USDT", "TRX/USDT", "LINK/USDT", "DOT/USDT", "MATIC/USDT", "TON/USDT", "DAI/USDT"],
        "kucoin": ["ARB/USDT", "MATIC/USDT", "OP/USDT", "LRC/USDT", "METIS/USDT", "STRK/USDT", "ETH/USDT", "BNB/USDT", "SOL/USDT", "ADA/USDT", "AVAX/USDT", "DOGE/USDT", "TRX/USDT", "LINK/USDT", "DOT/USDT", "MATIC/USDT", "TON/USDT", "DAI/USDT"],
        "binance": ["ARB/USDT", "MATIC/USDT", "OP/USDT", "LRC/USDT", "METIS/USDT", "STRK/USDT", "ETH/USDT", "BNB/USDT", "SOL/USDT", "ADA/USDT", "AVAX/USDT", "DOGE/USDT", "TRX/USDT", "LINK/USDT", "DOT/USDT", "MATIC/USDT", "TON/USDT", "DAI/USDT"],
        "ascendex": ["ARB/USDT", "MATIC/USDT", "OP/USDT", "LRC/USDT", "METIS/USDT", "STRK/USDT", "ETH/USDT", "BNB/USDT", "SOL/USDT", "ADA/USDT", "AVAX/USDT", "DOGE/USDT", "TRX/USDT", "LINK/USDT", "DOT/USDT", "MATIC/USDT", "TON/USDT", "DAI/USDT"],
        "bitget": ["ARB/USDT", "MATIC/USDT", "OP/USDT", "LRC/USDT", "METIS/USDT", "STRK/USDT", "ETH/USDT", "BNB/USDT", "SOL/USDT", "ADA/USDT", "AVAX/USDT", "DOGE/USDT", "TRX/USDT", "LINK/USDT", "DOT/USDT", "MATIC/USDT", "TON/USDT", "DAI/USDT"],
        "bitmart": ["ARB/USDT", "MATIC/USDT", "OP/USDT", "LRC/USDT", "METIS/USDT", "STRK/USDT", "ETH/USDT", "BNB/USDT", "SOL/USDT", "ADA/USDT", "AVAX/USDT", "DOGE/USDT", "TRX/USDT", "LINK/USDT", "DOT/USDT", "MATIC/USDT", "TON/USDT", "DAI/USDT"],
        "bitmex": ["ARB/USDT", "MATIC/USDT", "OP/USDT", "LRC/USDT", "METIS/USDT", "STRK/USDT", "ETH/USDT", "BNB/USDT", "SOL/USDT", "ADA/USDT", "AVAX/USDT", "DOGE/USDT", "TRX/USDT", "LINK/USDT", "DOT/USDT", "MATIC/USDT", "TON/USDT", "DAI/USDT"],
        "bybit": ["ARB/USDT", "MATIC/USDT", "OP/USDT", "LRC/USDT", "METIS/USDT", "STRK/USDT", "ETH/USDT", "BNB/USDT", "SOL/USDT", "ADA/USDT", "AVAX/USDT", "DOGE/USDT", "TRX/USDT", "LINK/USDT", "DOT/USDT", "MATIC/USDT", "TON/USDT", "DAI/USDT"],
        "coinex": ["ARB/USDT", "MATIC/USDT", "OP/USDT", "LRC/USDT", "METIS/USDT", "STRK/USDT", "ETH/USDT", "BNB/USDT", "SOL/USDT", "ADA/USDT", "AVAX/USDT", "DOGE/USDT", "TRX/USDT", "LINK/USDT", "DOT/USDT", "MATIC/USDT", "TON/USDT", "DAI/USDT"],
        "cryptocom": ["ARB/USDT", "MATIC/USDT", "OP/USDT", "LRC/USDT", "METIS/USDT", "STRK/USDT", "ETH/USDT", "BNB/USDT", "SOL/USDT", "ADA/USDT", "AVAX/USDT", "DOGE/USDT", "TRX/USDT", "LINK/USDT", "DOT/USDT", "MATIC/USDT", "TON/USDT", "DAI/USDT"],
        "gate": ["ARB/USDT", "MATIC/USDT", "OP/USDT", "LRC/USDT", "METIS/USDT", "STRK/USDT", "ETH/USDT", "BNB/USDT", "SOL/USDT", "ADA/USDT", "AVAX/USDT", "DOGE/USDT", "TRX/USDT", "LINK/USDT", "DOT/USDT", "MATIC/USDT", "TON/USDT", "DAI/USDT"],
        "kucoin": ["ARB/USDT", "MATIC/USDT", "OP/USDT", "LRC/USDT", "METIS/USDT", "STRK/USDT", "ETH/USDT", "BNB/USDT", "SOL/USDT", "ADA/USDT", "AVAX/USDT", "DOGE/USDT", "TRX/USDT", "LINK/USDT", "DOT/USDT", "MATIC/USDT", "TON/USDT", "DAI/USDT"],
        "mexc": ["ARB/USDT", "MATIC/USDT", "OP/USDT", "LRC/USDT", "METIS/USDT", "STRK/USDT", "ETH/USDT", "BNB/USDT", "SOL/USDT", "ADA/USDT", "AVAX/USDT", "DOGE/USDT", "TRX/USDT", "LINK/USDT", "DOT/USDT", "MATIC/USDT", "TON/USDT", "DAI/USDT"],
    }
    loops = [exchange_loop(exchange_id, symbols, profit_threshold) for exchange_id, symbols in exchanges.items()]
    await gather(*loops)

run(main())
