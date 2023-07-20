from src.read_data import Input
from time import time
import logging

if __name__ == '__main__':

    try:
        st = time()
        input_folder = 'input'
        output_folder = 'output'

        input = Input(input_folder=input_folder, output_folder=output_folder)
        input.generate_data()

        logging.info('Total running time: {}'.format(time() - st))

    except BaseException as e:
        logging.error('run daily job fail:', exc_info=True)
        raise e