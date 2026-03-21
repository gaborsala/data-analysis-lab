import returns_analysis
import volatility_analysis
import correlation_analysis
import drawdown_analysis
import rolling_metrics

def run():

    returns_analysis.run()
    volatility_analysis.run()
    correlation_analysis.run()
    drawdown_analysis.run()
    rolling_metrics.run()

    print("Pipeline finished successfully")


if __name__ == "__main__":
    run()