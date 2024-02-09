FROM nvidia/cuda:11.0.3-base-ubuntu20.04

RUN apt-get update && \
    apt-get install -y \
        git \
        python3-pip \
        python3-dev \
        libsndfile1

RUN python3 -m pip install --upgrade pip

RUN pip install git+https://github.com/m-bain/whisperX.git@a5dca2cc65b1a37f32a347e574b2c56af3a7434a
RUN pip install --no-build-isolation nemo_toolkit[asr]==1.21.0
RUN pip install git+https://github.com/facebookresearch/demucs#egg=demucs
RUN pip install deepmultilingualpunctuation
RUN pip install wget pydub
RUN pip install --force-reinstall torch torchaudio torchvision
RUN pip uninstall -y nvidia-cudnn-cu12
RUN pip install numba==0.58.0
RUN pip install unidecode
RUN pip install flask
RUN pip install python_dotenv

# Set the working directory
WORKDIR /app

# Copy the rest of your app's source code from your host to your image filesystem.
COPY src/ ./

# Expose port 5000
EXPOSE 5000

# Set the entrypoint
CMD ["python3", "app.py"]
