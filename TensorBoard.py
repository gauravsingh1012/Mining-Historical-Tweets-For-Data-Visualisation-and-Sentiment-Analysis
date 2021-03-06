import datetime
import tensorflow as tf
from tensorboardcolab import *
import shutil
import os
#PUT THIS IN A SEPARATE CELL

class TensorBoard(object):
    """
    TensorBoard is a visualization tool provided with TensorFlow.
    This class can be used to record attributes from a running
    Zipline algorithm.
    """

    def __init__(self):
        tbc = TensorBoardColab()
        shutil.rmtree('./Graph',ignore_errors=True)
        os.mkdir('./Graph')
        self.writer = tbc.get_writer()
        print("TensorBoard Initialized")

    def log_dict(self, epoch, logs):
        """
        Writes a dictionary of simple named values to TensorBoard.
        Args:
            epoch: An integer representing time.
            logs: A dict containing what we want to log to TensorBoard.
        """

        graph = tf.Graph()
        with tf.Session(graph=graph) as sess:
            for name, value in logs.items():
                #summary = tf.Summary()
                #summary_value = summary.value.add()
                #summary_value.simple_value = value
                #summary_value.tag = name
                tf.summary.scalar(name, value)
                tf_summary = tf.summary.merge_all()
                summary = tf_summary.eval()
                self.writer.add_summary(summary, global_step=epoch)
            self.writer.flush()

    def log_algo(self, algo, epoch=None, other_logs={}):
        """
        Logs info about a Zipline algorithm as it's running.
        Args:
            epoch: An integer representing algorithm time.
                   If None, then the algorithm's current
                   date is converted to an ordinal so that
                   these integers are monotonically increasing
                   with time. The same integer convention should
                   be used across different runs so that their charts
                   line up correctly.
           algo: An instance of a zipline.algorithm.TradingAlgorithm
           other_logs: A dictionary containing other things we want to log.
        """
        if epoch is None:
            epoch = datetime.date.toordinal(algo.get_datetime())

        logs = {}

        # add portfolio related things
        logs['portfolio_value'] = algo.portfolio.portfolio_value
        logs['portfolio_pnl'] = algo.portfolio.pnl
        logs['portfolio_return'] = algo.portfolio.returns
        logs['portfolio_cash'] = algo.portfolio.cash
        logs['portfolio_capital_used'] = algo.portfolio.capital_used
        logs['portfolio_positions_exposure'] = algo.portfolio.positions_exposure
        logs['portfolio_positions_value'] = algo.portfolio.positions_value
        logs['number_of_orders'] = len(algo.blotter.orders)
        logs['number_of_open_orders'] = len(algo.blotter.open_orders)
        logs['number_of_open_positions'] = len(algo.portfolio.positions)

        # add recorded variables from `zipline.algorithm.record` method
        for name, value in algo.recorded_vars.items():
            logs[name] = value

        # add any extras passed in through `other_logs` dictionary
        for name, value in other_logs.items():
            logs[name] = value

        self.log_dict(epoch, logs)
