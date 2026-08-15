# Limit-Order-Book-Matching-Engine-Price-Time-Priority-Execution-Simulator
A quantitative trading and market microstructure simulation project that
implements a simplified limit order book and matching engine using
price-time priority, market orders, limit orders, partial fills, and
execution simulation.

## Project Overview

This project implements a simplified electronic market matching system.

The simulator:

1. Creates buy and sell orders.
2. Maintains a central limit order book.
3. Organizes orders using price-time priority.
4. Matches compatible buy and sell orders.
5. Supports market and limit orders.
6. Handles complete and partial fills.
7. Tracks remaining order quantities.
8. Generates executed trades.
9. Calculates best bid and best ask.
10. Calculates mid-price and bid-ask spread.
11. Calculates execution VWAP.
12. Tracks total executed volume.
13. Maintains trade history.
14. Simulates basic market microstructure.

## Core Concepts

### Limit Order Book

A limit order book maintains outstanding buy and sell orders.

The book contains two primary sides:

```text
BUY SIDE  → Bids
SELL SIDE → Asks
Price-Time Priority
The matching engine follows price-time priority.
For buy orders:
Higher price → Higher priority
For sell orders:
Lower price → Higher priority
When multiple orders have the same price:
Earlier order → Higher priority
Therefore, execution priority is determined first by price and then by the time at which the order entered the book.
Conceptually:
Buy Side:

Higher Price
     |
     v
Price Priority
     |
     v
Earlier Timestamp
     |
     v
Execution Priority
Market Orders
A market order does not specify a limit price.
Instead, it consumes available liquidity from the opposite side of the order book.
For example:
BUY MARKET 15
will consume the lowest available sell prices first.
If the sell side contains:
SELL 5 @ 100.00
SELL 7 @ 100.00
SELL 10 @ 100.50
the market buy order can execute as:
5 @ 100.00
7 @ 100.00
3 @ 100.50
Limit Orders
A limit order specifies an acceptable execution price.
Example:
BUY 10 @ 99.50
The order can execute only when a compatible sell order is available at 99.50 or better.
If the order cannot execute immediately, the remaining quantity stays in the order book as resting liquidity.
Partial Fills
An order can be partially filled when available liquidity is smaller than the requested order quantity.
For example:
SELL 5 @ 100.00
A market buy order for:
BUY MARKET 10
can execute:
5 @ 100.00
The remaining:
5 units
remain unfilled.
This demonstrates partial execution and liquidity constraints.
Order Matching Process
The matching engine follows this process:
Incoming Order
      |
      v
Identify Order Type
      |
      v
Check Opposite Side
      |
      v
Find Best Available Price
      |
      v
Check Price Condition
      |
   +--+--+
   |     |
  Yes    No
   |     |
   v     v
Execute  Rest Limit
Trade    Order
   |
   v
Update Quantities
   |
   v
Remaining Quantity?
   |
  +--+
  |  |
 Yes No
  |   |
  v   v
Next  Order
Level Filled
Market Microstructure
The simulator calculates several important market microstructure variables.
Best Bid
The highest available buy price.
Best Bid = Maximum Bid Price
The best bid represents the highest price currently offered by buyers.
Best Ask
The lowest available sell price.
Best Ask = Minimum Ask Price
The best ask represents the lowest price currently offered by sellers.
Mid Price
The midpoint between the best bid and best ask.
Mid Price =
(Best Bid + Best Ask) / 2
The mid price provides a simple estimate of the current market center.
Bid-Ask Spread
The bid-ask spread measures the difference between the best ask and best bid.
Spread =
Best Ask - Best Bid
A smaller spread generally indicates tighter displayed liquidity.
Market Depth
Market depth represents the quantity of available liquidity at different price levels.
Example:
ASKS

100.50 | 10
100.00 | 12

BIDS

 99.50 | 8
 99.00 | 10
The order book therefore provides information about available liquidity at multiple price levels.
Execution Simulation
The project creates a deterministic execution scenario.
The simulation includes:
Initial sell-side liquidity.
Initial buy-side liquidity.
Market order execution.
Limit-order execution.
Partial fills.
Multiple price-level executions.
Trade generation.
Order-book updates.
Execution statistics.
Example initial liquidity:
SELL 5 @ 100.00
SELL 7 @ 100.00
SELL 10 @ 100.50

BUY 8 @ 99.50
BUY 10 @ 99.00
An incoming market buy order:
BUY MARKET 15
can consume:
5 @ 100.00
7 @ 100.00
3 @ 100.50
The remaining sell liquidity becomes:
7 @ 100.50
This demonstrates how a single incoming order can interact with multiple resting orders.
Execution Price
The execution price of a trade is determined by the resting order that provides liquidity.
For example:
Resting SELL 5 @ 100.00
Incoming BUY MARKET 5
results in:
Execution Price = 100.00
This models a fundamental principle of order-book-based execution.
Execution VWAP
The simulator calculates the volume-weighted average execution price.
The formula is:
VWAP =
Σ(Execution Price × Execution Quantity)
----------------------------------------
        Σ(Execution Quantity)
VWAP provides a summary of the average price at which executed volume was traded.
Trade History
Every successful execution creates a trade record containing:
Trade ID
Buy order ID
Sell order ID
Execution price
Execution quantity
Execution timestamp
Example:
Trade ID
   |
   +---- Buy Order ID
   |
   +---- Sell Order ID
   |
   +---- Execution Price
   |
   +---- Execution Quantity
   |
   +---- Timestamp
The trade history allows the simulation to analyze completed executions.
Order Cancellation
The matching engine supports order cancellation.
An active order can be cancelled before its remaining quantity is executed.
After cancellation, the order is no longer considered active for execution.
Project Architecture
The system is divided into separate modules:
Order Definitions
       |
       v
Limit Order Book
       |
       v
Matching Engine
       |
       v
Execution Simulation
       |
       v
Trade History
       |
       v
Market Microstructure Metrics
This modular design separates order management, matching logic, simulation, and performance analysis.
Project Structure
limit-order-book-matching-engine/
│
├── README.md
├── main.py
├── order_book.py
├── orders.py
├── execution.py
├── metrics.py
├── requirements.txt
└── .gitignore
File Descriptions
main.py
Main entry point of the project.
Runs the complete limit order book and matching-engine simulation.
It:
Starts the simulation.
Creates the order book.
Processes orders.
Displays the order book.
Calculates market statistics.
Displays execution statistics.
Displays trade history.
orders.py
Contains the order definitions.
Implements:
Buy orders
Sell orders
Market orders
Limit orders
Order quantities
Remaining quantities
Order timestamps
Order filling
Order cancellation
Order state management
order_book.py
Contains the main limit order book and matching engine.
Implements:
Bid-side order management
Ask-side order management
Price-time priority
Market-order matching
Limit-order matching
Partial fills
Trade generation
Order cancellation
Best bid
Best ask
Mid price
Market depth
Trade history
execution.py
Contains the execution simulation.
It generates a deterministic sequence of orders to demonstrate:
Resting liquidity
Market orders
Limit orders
Partial fills
Multiple price-level executions
Crossing orders
Execution flow
metrics.py
Calculates market microstructure and execution statistics.
It includes:
Bid-ask spread
Mid price
Execution VWAP
Total executed volume
Execution cost
requirements.txt
Contains the Python dependency information required to run the project.
The current implementation uses Python standard-library modules and does not require external packages.
.gitignore
Contains files and folders that should not be uploaded to GitHub.
Examples include:
Python cache files
Virtual environments
IDE configuration files
Local environment files
Mathematical Framework
Mid Price
The mid price is calculated as:
P_mid =
(P_bid + P_ask) / 2
where:
P_bid = Best Bid
P_ask = Best Ask
Bid-Ask Spread
The spread is calculated as:
Spread =
P_ask - P_bid
Volume-Weighted Average Price
Execution VWAP is:
VWAP =
Σ(P_i × Q_i)
---------
ΣQ_i
where:
P_i = Execution Price
Q_i = Execution Quantity
Total Executed Volume
Total executed volume is:
Total Volume =
Σ Execution Quantity
Installation
Clone the repository:
git clone https://github.com/thirupathikannan-ai/limit-order-book-matching-engine.git
Enter the project directory:
cd limit-order-book-matching-engine
Check the Python version:
python --version
Python 3.10 or newer is recommended.
Install the project requirements:
pip install -r requirements.txt
The project currently uses Python standard-library functionality, so no external packages are required.
Running the Project
Run the matching-engine simulation using:
python main.py
The program displays:
Limit order book
Best bid
Best ask
Mid price
Bid-ask spread
Number of executed trades
Total executed volume
Execution VWAP
Trade history
Quantitative Trading Architecture
Market Participants
        |
        v
Incoming Orders
        |
        v
+-------------------------+
|   Limit Order Book      |
|                         |
| Bids        Asks        |
+-------------------------+
        |
        v
Price-Time Priority
        |
        v
Matching Engine
        |
        +----------------+
        |                |
        v                v
   Executed Trade    Resting Order
        |                |
        v                v
   Trade History    Order Book
        |
        v
Market Microstructure
        |
        +----------------------+
        |          |           |
        v          v           v
     Spread     Mid Price    VWAP
        |
        v
Execution Analysis
============================================================
 LIMIT ORDER BOOK & MATCHING ENGINE
============================================================

Running execution simulation...

=======================================================
LIMIT ORDER BOOK
=======================================================

ASKS
-------------------------

-------------------------
-------------------------

BIDS
-------------------------
Price:   100.50 | Quantity:     5
Price:    99.50 | Quantity:     3
Price:    99.00 | Quantity:    10
=======================================================

MARKET MICROSTRUCTURE
----------------------------------------
Best Bid          : 100.50
Best Ask          : None
Mid Price         : None
Bid-Ask Spread    : None

EXECUTION STATISTICS
----------------------------------------
Total Trades      : 5
Total Volume      : 27
Execution VWAP    : 100.0926

EXECUTED TRADES
-----------------------------------------------------------------
Trade   1 | Price:   100.00 | Qty:    5 | Buy:   6 | Sell:   1
Trade   2 | Price:   100.00 | Qty:    7 | Buy:   6 | Sell:   2
Trade   3 | Price:   100.50 | Qty:    3 | Buy:   6 | Sell:   3
Trade   4 | Price:    99.50 | Qty:    5 | Buy:   4 | Sell:   7
Trade   5 | Price:   100.50 | Qty:    7 | Buy:   8 | Sell:   3

============================================================
 SIMULATION COMPLETED SUCCESSFULLY
============================================================
Learning Outcomes
This project demonstrates practical understanding of:
Limit order books
Price-time priority
Market orders
Limit orders
Order matching
Partial fills
Market microstructure
Liquidity
Price discovery
Bid-ask spread
Mid-price calculation
Execution VWAP
Trade generation
Order cancellation
Execution simulation
Data structures
Algorithms
Quantitative trading
Algorithmic execution
Quantitative Trading Relevance
Limit order books are fundamental components of modern electronic financial markets.
This project demonstrates how buy and sell orders interact with available liquidity and how execution prices are determined according to price-time priority.
The project connects software engineering with quantitative trading concepts including:
Market microstructure
Liquidity
Price discovery
Order priority
Execution
Trading simulation
Execution analysis
Quantitative programming
Educational Purpose
This project is intended to demonstrate the fundamental mechanics of an electronic order-driven market.
It is designed for educational and research purposes and does not connect to a live financial exchange.
Disclaimer
This project is intended for educational and research purposes only.
It is not financial advice and should not be used as a live trading system without appropriate testing, validation, monitoring, and risk controls.
Author
Thirupathi Kannan K
B.E. Electronics and Communication Engineering
Areas of Interest:
Quantitative Trading
Quantitative Finance
Probability and Statistics
Algorithmic Trading
Market Microstructure
Trading Systems
Machine Learning
