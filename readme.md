\#Project overview (problem, audience, value)  
\#\#This project was developed as an extension of our previous group project, which was a chart that displayed different ticker symbols that represented crypto currency (Bitcoin in US Dollars), tangible assets (Gold), stocks (S\&P 500), and the CBOE Volatility Index.  We then had a simple correlation matrix that printed in the terminal.  The purpose of this was to see if there was any sort of correlation between the movement of each of those individual ticker symbols.  This project has a primary purpose of allowing people to do some basic research on a stock of their choice and then generate a chart and correlation matrix on the fly.  The Volatility Index and S\&P 500 are prefilled but the user is able to enter as many as two stocks of their choice.  

\#\#Problem:  
\#\#\#Individual investors often struggle to interpret stock movements. Without context, a single stock chart can be misleading, leading to poor decisions  
\#\#Audience:  
\#\#\#Our platform is designed for investors who want a clearer picture of how their chosen stock behaves relative to market volatility.  
\#\#Value:  
\#\#\#By allowing users to compare their stock of choice against the VIX(a volatility index that represents market’s expectation of volatility based on S\&P 500 index options), our platform provides essential context for decision making. The correlation matrix and the comparison graph empowers users to distinguish company performance from market wide trends, helping them make better investment choice. 

\#How to run (local \+ deploy notes):

1. Download zip file and extract all files to your local directory.  
2. Open “app.py”.  
3. Ensure the following are installed (they can be installed using the pip command):  
   1. “dash”  
   2. “dash\_bootstrap\_components”  
   3. “plotly.express”  
   4. “yfinance”  
   5. “pandas”  
   6. “requests”  
   7. “datetime”  
4. Run “app.py”  
5. Once running the user can access the following pages:  
   1. Home: Brief description of the application and its intended purpose.  
   2. Research: Allows the user to input a stock either by name or by ticker symbol ((e.g., “Apple” or “AAPL”). The output will provide the user with its closing price over the last year and a background summary of the stock.  
   3. Comparisons:Allows the user to input up to two (2) stocks to compare to the S\&P 500 and VIX tickers over a user selected time period.. The result will be a graph and accompanying table showing the correlation between the graphed stocks.  
   4.  About us: Information about the development team.  
   5. Note: stock is used throughout this text however ticker symbols as used by Yahoo Finance are acceptable (e.g. Bitcoin USD Price listed as BTC-USD).  
      

\#Data sources & data dictionary \-   
\#\#\#yfinance 0.2.65 unofficial API was used.    
\#\#\#Details can be found at this url \- [https://pypi.org/project/yfinance/](https://pypi.org/project/yfinance/)

