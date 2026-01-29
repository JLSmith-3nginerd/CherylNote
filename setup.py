from setuptools import setup, find_packages

setup(
    name="audio-transcription-app",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "torch>=1.9.0",
        "torchaudio>=0.9.0", 
        "librosa>=0.8.0",
        "soundfile>=0.10.3"
    ],
    entry_points={
        'console_scripts': [
            'audio-transcriber=main:main',
        ],
    },
)