from analyzer.data_checker import DataChecker
from data_transfer.advanced_collector import AdvancedStats
from data_transfer.traditional_collector import TraditionalStats


if __name__ == "__main__":
    datachecker = DataChecker()
    advanced = AdvancedStats()
    traditional = TraditionalStats()

    advanced.run()
    traditional.run()
    datachecker.runner()
