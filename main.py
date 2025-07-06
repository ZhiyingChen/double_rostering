import sys

from src.data import Input
from src.alns import ALNSEnv
from src.dump import Dump
from time import time
import logging

if __name__ == '__main__':

    try:
        st = time()
        input_folder = 'input'
        if 'win' in sys.platform:
            output_folder = './output/'
        else:
            output_folder = '/tmp/'

        input_data = Input(
            input_folder=input_folder, output_folder=output_folder
        )
        input_data.generate_data()

        ALNSMethod = ALNSEnv(input=input_data)
        ALNSMethod.run()

        dumper = Dump(data=input_data)
        result_df = dumper.generate_output_df()

        logging.info('Total running time: {}'.format(time() - st))

    except BaseException as e:
        logging.error('run daily job fail:', exc_info=True)
        raise e
