import json

from src.lib.dejavu.dejavu import Dejavu
from src.lib.dejavu.dejavu.recognize import FileRecognizer
from src.utilities.data_utils import load_program_boundary_files
from src import ROOT_DIR

from pydub import AudioSegment


AUDIO_PATH = ROOT_DIR + '/../data/example/'
AUDIO_SEGMENT_PATH = ROOT_DIR +  '/../data/example/audio_seg.mp3'
CUTFILE_PATH = ROOT_DIR + '/../data/example/example.cuts'


class FingerPrint(object):
    """docstring for FingerPrint"""
    def __init__(self, dejavu_config_path="dejavu.cnf"):
        super(FingerPrint, self).__init__()
        # load config from a JSON file (or anything outputting a python dictionary)
        with open(dejavu_config_path) as f:
            config = json.load(f)
        self.dejavu = Dejavu(config) 
        # create audiofingerprint for all audio files in the directory


    def slice_audio_segment(self, filename, start, end, audio_format="mp3"):
        audiofile = AudioSegment.from_file(filename, audio_format)
        audio_segment = audiofile[start * 1000: end * 1000]
        audio_segment.export(AUDIO_SEGMENT_PATH, format=audio_format, tags={})


    def extract_fingerprint_single(self, filepath=AUDIO_SEGMENT_PATH):        
        # will automatically save extracted fingerprint
        self.dejavu.fingerprint_file(filepath)


    def extract_fingerprint_directory(self, filepath=AUDIO_PATH):
        # extract all mp3 segment files
        # TODO: create /seg folder to extract only from seg files
        self.dejavu.fingerprint_directory(filepath, [".mp3"])


    def recognize_audio(self, filename):
        song = self.dejavu.recognize(FileRecognizer, filename)
        print("From file we recognized: %s\n" % song)
        return song


    def slice_with_cutfiles(self, cut_filepath, audio_filepath):
        # TODO: handle segment duplicate
        files = load_program_boundary_files(cut_filepath)        
        boundaries, _ = next(files)

        a = boundaries.iloc[0]
        pad = 10 # 10 secs
        for index, row in boundaries.iterrows():
            b = row['t_program_boundary']
            dt = a - b
            secs = dt.item().total_seconds()
            self.slice_audio_segment(audio_filepath, secs - pad, secs + pad)
