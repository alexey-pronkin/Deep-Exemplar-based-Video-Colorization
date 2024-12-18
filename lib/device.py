import os, logging
import torch

logger = logging.getLogger(__name__)


# select the device for computation
def get_device():
    force_cpu_device = os.environ.get("FORCE_CPU_DEVICE", "0") == "1"
    if force_cpu_device:
        logger.info("forcing CPU device")
    if torch.cuda.is_available() and not force_cpu_device:
        device = torch.device("cuda")
    elif torch.backends.mps.is_available() and not force_cpu_device:
        device = torch.device("mps")
    else:
        device = torch.device("cpu")
    logger.info(f"using device: {device}")

    if device.type == "cuda":
        # turn on tfloat32 for Ampere GPUs (https://pytorch.org/docs/stable/notes/cuda.html#tensorfloat-32-tf32-on-ampere-devices)
        if torch.cuda.get_device_properties(0).major >= 8:
            torch.backends.cuda.matmul.allow_tf32 = True
            torch.backends.cudnn.allow_tf32 = True
    elif device.type == "mps":
        logging.warning(
            "\nSupport for MPS devices is preliminary. SAM 2 is trained with CUDA and might "
            "give numerically different outputs and sometimes degraded performance on MPS. "
            "See e.g. https://github.com/pytorch/pytorch/issues/84936 for a discussion."
        )

    return device
