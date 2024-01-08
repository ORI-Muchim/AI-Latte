import matplotlib.pyplot as plt
import os
import json
import math
import time
import torch
import sys
from torch import nn
from torch.nn import functional as F
from torch.utils.data import DataLoader
import commons
import utils
from data_utils import TextAudioLoader, TextAudioCollate, TextAudioSpeakerLoader, TextAudioSpeakerCollate
from models import SynthesizerTrn
from text.symbols import symbols
from text import text_to_sequence
from scipy.io.wavfile import write

device = 'cpu'
    
def get_text(text, hps):
    text_norm = text_to_sequence(text, hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = torch.LongTensor(text_norm)
    return text_norm

hps = utils.get_hparams_from_file("./models/latte/config.json")

net_g = SynthesizerTrn(
    len(symbols),
    hps.data.filter_length // 2 + 1,
    hps.train.segment_size // hps.data.hop_length,
    **hps.model).to(device)
_ = net_g.eval()

_ = utils.load_checkpoint("./models/latte/G_107000.pth", net_g, None)

output_dir = './vitsoutput/latte'
os.makedirs(output_dir, exist_ok=True)

speaker = 'latte'

def voice_gen(response):
    stn_tst = get_text(response, hps)
    with torch.no_grad():
        timestamp = int(time.time())
        print("음성 생성 중...", response)
        x_tst = stn_tst.to(device).unsqueeze(0)
        x_tst_lengths = torch.LongTensor([stn_tst.size(0)]).to(device)
        audio = net_g.infer(x_tst, x_tst_lengths, noise_scale=.667, noise_scale_w=0.8, length_scale=1)[0][0,0].data.cpu().float().numpy()
        filename = f'{output_dir}/{speaker}_{timestamp}.wav'
        write(filename, hps.data.sampling_rate, audio)
        print(f'{filename} Generated!')
        return filename

