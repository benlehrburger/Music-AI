# Author: Ben Lehrburger
# Project: Music & AI
# Script: Combine the vocal track and backtrack

import warnings

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    from pydub import AudioSegment


# Overlay vocal track on top of backtrack
def overlay(vocal_path, backtrack_path, outputPath, vocalBoost=0, backtrackBoost=0):

    backtrack = AudioSegment.from_file(backtrack_path)
    backtrack += backtrackBoost
    vocals = AudioSegment.from_file(vocal_path)
    vocals += vocalBoost
    combined = backtrack.overlay(vocals)
    combined.export(outputPath, format='wav')
