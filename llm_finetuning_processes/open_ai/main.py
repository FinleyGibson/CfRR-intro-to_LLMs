"""
Based on:
   https://www.datacamp.com/tutorial/fine-tuning-openais-gpt-4-step-by-step-guide
"""

import logging
import os
from pathlib import Path

from openai import OpenAI

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Set the OPENAI_API_KEY environment variable
os.environ["OPENAI_API_KEY"] = (
    "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"
)


def upload_training_data(client: OpenAI, jsonl_path: str | Path):
    return client.files.create(file=open(str(jsonl_path), "rb"), purpose="fine-tune")


def fine_tune(client: OpenAI, model_name: str, data_id: str):
    client.fine_tuning.jobs.create(training_file=data_id, model=model_name)


def main():
    data_path = Path("assets/train.jsonl")
    out_path = Path("file-rIua39sJX1O64gzxTYfpvJx7")
    model = "gpt-3.5-turbo"  # change to gpt-4-0613 if you have access

    client = OpenAI()

    training_data = upload_training_data(client, data_path)
    logger.info("Training file uploaded: id=%s", training_data.id)

    logger.info("Starting fine-tuning job: model=%s, training_file=%s", model, training_data.id)
    tuning_out = fine_tune(client, model, training_data.id)
    logger.info("Fine-tuning job created: %s", tuning_out)


if __name__ == "__main__":
    main()
