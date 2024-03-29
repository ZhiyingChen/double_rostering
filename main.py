from src.data import Input
from src.alns import ALNSEnv
from src.dump import Dump
from time import time
import logging

if __name__ == '__main__':

    try:
        st = time()
        input_folder = 'input'
        output_folder = 'output'

        input = Input(input_folder=input_folder, output_folder=output_folder)
        input.generate_data()

        ALNSMethod = ALNSEnv(input=input)
        ALNSMethod.run()

        dumper = Dump(data=input)
        dumper.generate_output_df()

        logging.info('Total running time: {}'.format(time() - st))

    except BaseException as e:
        logging.error('run daily job fail:', exc_info=True)
        raise e