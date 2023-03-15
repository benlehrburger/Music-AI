# Music & AI
Map your own voice to AI-generated music tracks! Final project submission for COSC 89.29 (Music & AI). Script is intended to be an augmentation tool used alongside other AI-generated music platforms like AIVA or Amper.

# Quick Resources
- [Input Examples](https://github.com/benlehrburger/musicAI/tree/main/Audio%20Input/Example)
- [Output Examples](https://github.com/benlehrburger/musicAI/tree/main/Audio%20Output)

# Set Up
1) Download repository
2) Install dependencies
```python
pip install -r Config/requirements.txt
```

# Run Example
1) Open project in your preferred IDE (you can run from commandline but may run into errors with the Librosa dependency)
2) Run [execute.py](https://github.com/benlehrburger/musicAI/blob/main/execute.py)
3) When prompted for name of vocal input file, input <i>example</i> to run the example
4) Outputs will be saved to the [Audio Output](https://github.com/benlehrburger/musicAI/tree/main/Audio%20Output) folder

# Create Your Own Project
1) Add your vocal sample file (.wav/.mp3) to [Audio Input](https://github.com/benlehrburger/musicAI/tree/main/Audio%20Input) directory
2) Add your backtrack file (.wav/.mp3) to [Audio Input](https://github.com/benlehrburger/musicAI/tree/main/Audio%20Input) directory
3) Add your vocal melody file (.mid) to [Audio Input](https://github.com/benlehrburger/musicAI/tree/main/Audio%20Input) directory
4) Run [execute.py](https://github.com/benlehrburger/musicAI/blob/main/execute.py)
5) When prompted for names of your three input files (one at a time), input the <i>relative-path-to-your-file</i>

# Code Cited

- TheWolfSound. (n.d.). How to Auto-Tune Your Voice with Python. Retrieved March 15, 2023, from https://thewolfsound.com/how-to-auto-tune-your-voice-with-python/
- Kumar, A. (2019, September 6). Speech Recognition with Timestamps. Towards Data Science. Retrieved March 15, 2023, from https://towardsdatascience.com/speech-recognition-with-timestamps-934ede4234b2

