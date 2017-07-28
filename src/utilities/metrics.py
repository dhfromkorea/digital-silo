import numpy as np
from src.utilities.data_utils import *


def _evaluate_accuracy(y, pred):
    TP = (y & pred).sum() 
    TN = (~y & ~pred).sum()
    FP = (~y & pred).sum()
    FN = (y & ~pred).sum()
    if pred.sum() != (TP + FP):
        print('something is wrong with predictions')
    return (TP, TN, FP, FN)

def accuracy_score_f1(model, X_path, y_path=None):
    '''[summary]
    
    [description]
    
    Args:
        model: [description]
        X_path: [root path for caption files]
        y_path: [root path for cut files] (default: {the same as X_path})
    
    Returns:
        [description]
        [type]
    '''
    caption_files = load_caption_files(X_path, keep_story_boundary=True)
    results = []

    total_TP = 0    
    total_FP = 0
    total_FN = 0
    num_caption_files = 0
    for caption_file in caption_files:
        caption, metadata = caption_file
        if caption.empty:
            print("an empty caption file: {}".format(caption))
            continue

        X = split_caption_to_X(caption)
        print('processing', metadata['filename'])
        if y_path == None:
            y_path = X_path
        y_file_path = find_y_path_from_X_filename(metadata['filename'], y_path)
        p_boundaries, _ = next(load_program_boundary_files(y_file_path))
        y = convert_program_boundaries_to_y(p_boundaries, X)

        #TODO: decision unit and this is not a true f1 score
        #decision unit (for classification) should be roughly the same as grace period?
        pred = model.predict(X)
        

        (TP, TN, FP, FN) = _evaluate_accuracy(y, pred)


        # get a sense of why recall isn't 100%
        # if FN > 0:
        #     print(metadata['filename'])
        #     indices = y[y & ~pred].index
            

        accuracy = (TP + TN) / len(pred)
        msg = 'accuracy: {}\nTP: {}\nTN: {}\nFP: {}\nFN: {}\n'
        # print(msg.format(accuracy, TP, TN, FP, FN))

        total_TP += TP
        total_FP += FP
        total_FN += FN
        num_caption_files += 1

    recall = total_TP / (total_TP + total_FN)
    precision = total_TP / (total_TP + total_FP)
    f1_score = 2*(precision*recall)/(precision + recall)
    msg = 'overall performance:\nprecision: {} \
           \nrecall: {}\nf1: {}\ntotal caption files predicted: {}\n'
    print(msg.format(precision, recall, f1_score, num_caption_files))
    # return more detailed report like showing failure cases    
    return f1_score