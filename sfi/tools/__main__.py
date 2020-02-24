from pathlib import Path

import argparse

import sfi.tools.frames
import sfi.tools.feature
import sfi.tools.feature3d
import sfi.tools.stream
import sfi.tools.server
import sfi.tools.client
import sfi.tools.train
import sfi.tools.infer
import sfi.tools.export

parser = argparse.ArgumentParser(prog="sficmd")
subcmd = parser.add_subparsers(title="commands", metavar="")
subcmd.required = True

Fmt = argparse.ArgumentDefaultsHelpFormatter

frames = subcmd.add_parser("save-frames", help="saves key frames for video", formatter_class=Fmt)
frames.add_argument("--video", type=Path, required=True, help="file load video from")
frames.add_argument("--frames", type=Path, required=True, help="directory to save key frames to")
frames.add_argument("--similarity", type=float, default=0.95, help="similarity key frame threshold")
frames.add_argument("--pool", choices=["mean", "max"], default="mean", help="spatial pooling mode")
frames.add_argument("--image-size", type=int, default=7 * 32, choices=[v * 32 for v in range(1, 15)])
frames.add_argument("--batch-size", type=int, default=8)
frames.set_defaults(main=sfi.tools.frames.main)

stream = subcmd.add_parser("stream-index", help="builds an index in streaming mode", formatter_class=Fmt)
stream.add_argument("--index", type=Path, required=True, help="file to save index to")
stream.add_argument("--frames", type=Path, required=True, help="directory to load image frames from")
stream.add_argument("--num-train", type=int, required=True, help="number of samples to train on")
stream.add_argument("--image-size", type=int, default=14 * 32, choices=[v * 32 for v in range(1, 15)])
stream.add_argument("--batch-size", type=int, default=64)
stream.add_argument("--num-workers", type=int, default=0)
stream.set_defaults(main=sfi.tools.stream.main)

feature = subcmd.add_parser("save-feature", help="saves features for frames", formatter_class=Fmt)
feature.add_argument("--frame", type=Path, required=True, help="path to image frame")
feature.add_argument("--feature", type=Path, required=True, help="path to save features to")
feature.add_argument("--image-size", type=int, default=14 * 32, choices=[v * 32 for v in range(1, 15)])
feature.set_defaults(main=sfi.tools.feature.main)

feature3d = subcmd.add_parser("save-feature3d", help="saves features for videos", formatter_class=Fmt)
feature3d.add_argument("--video", type=Path, required=True, help="path to video")
feature3d.add_argument("--feature", type=Path, required=True, help="path to save features to")
feature3d.add_argument("--timesteps", type=int, default=64, help="frames per sequence along time axis")
feature3d.set_defaults(main=sfi.tools.feature3d.main)

server = subcmd.add_parser("query-server", help="starts up the index query http server", formatter_class=Fmt)
server.add_argument("--index", type=Path, required=True, help="file to load index from")
server.add_argument("--host", type=str, default="127.0.0.1")
server.add_argument("--port", type=int, default=5000)
server.add_argument("--num-probes", type=int, default=1, help="number of cells to visit during search")
server.add_argument("--features-size", type=int, default=1, choices=range(1, 15))
server.set_defaults(main=sfi.tools.server.main)

client = subcmd.add_parser("query-client", help="queries the query server for similar features", formatter_class=Fmt)
client.add_argument("--host", type=str, default="127.0.0.1")
client.add_argument("--port", type=int, default=5000)
client.add_argument("--query", type=Path, required=True, help="feature file to query the index with")
client.add_argument("--num-results", type=int, default=10, help="number of similar frames to query for")
client.set_defaults(main=sfi.tools.client.main)

train = subcmd.add_parser("model-train", help="trains a classifier model", formatter_class=Fmt)
train.add_argument("--model", type=Path, required=True, help="file to save trained model to")
train.add_argument("--resume-from", type=Path, help="file to load trained model from")
train.add_argument("--dataset", type=Path, required=True, help="directory to load dataset from")
train.add_argument("--batch-size", type=int, default=24)
train.add_argument("--num-workers", type=int, default=0)
train.add_argument("--num-epochs", type=int, default=100)
train.set_defaults(main=sfi.tools.train.main)

infer = subcmd.add_parser("model-infer", help="runs inference with a classifier model", formatter_class=Fmt)
infer.add_argument("--model", type=Path, required=True, help="file to load trained model from")
infer.add_argument("--dataset", type=Path, required=True, help="directory to load dataset from")
infer.add_argument("--results", type=Path, required=True, help="file to save results to")
infer.add_argument("--batch-size", type=int, default=64)
infer.add_argument("--num-workers", type=int, default=0)
infer.set_defaults(main=sfi.tools.infer.main)

export = subcmd.add_parser("model-export", help="export a classifier model to onnx", formatter_class=Fmt)
export.add_argument("--model", type=Path, required=True, help="file to load trained model from")
export.add_argument("--onnx", type=Path, required=True, help="file to save trained onnx model to")
export.set_defaults(main=sfi.tools.export.main)

args = parser.parse_args()
args.main(args)
