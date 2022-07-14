import torch
from inference import convert_video

model = torch.hub.load("PeterL1n/RobustVideoMatting", "mobilenetv3").cpu() # or "resnet50"


def video_matting(                   
        input_source='input.mp4',        # A video file or an image sequence directory.
        output_composition='com.mp4',
        output_alpha="pha.mp4",          # [Optional] Output the raw alpha prediction.
        output_foreground="fgr.mp4", ):
    convert_video(
        model,                           # The model, can be on any device (cpu or cuda).
        input_source=input_source,        # A video file or an image sequence directory.
        output_type='video',             # Choose "video" or "png_sequence"
        output_composition=output_composition,    # File path if video; directory path if png sequence.
        output_alpha=output_alpha,          # [Optional] Output the raw alpha prediction.
        output_foreground=output_foreground,     # [Optional] Output the raw foreground prediction.
        output_video_mbps=4,             # Output video mbps. Not needed for png sequence.
        downsample_ratio=None,           # A hyperparameter to adjust or use None for auto.
        seq_chunk=12,                    # Process n frames at once for better parallelism.
    )

# video_matting()