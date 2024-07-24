"""
This module contains the main Flask application.

It defines routes for handling user requests to merging csv files.
"""

import os
from typing import List
from flask import Flask, jsonify, request, send_file, after_this_request
from werkzeug.datastructures import FileStorage

from logger.logger_factory import LoggerFactory
from controllers.csv_merger import CsvMerger
from services.file_service import FileService
from services.input_sanitizer_service import InputSanitizerService

app = Flask(__name__)

logger = LoggerFactory.get_logger(__name__)

UPLOAD_FOLDER = "./reports/uploads"


@app.route("/")
def hello_world():
    """Welcome endpoint"""
    return jsonify({"message": "Welcome to the CSV Merger API"}), 200


@app.route("/health")
def health():
    """Health endpoint"""
    logger.info("Received health GET request")
    return jsonify({"message": "Healthy"}), 200


@app.route("/csvs", methods=["POST"])
def csvs():
    """Merge multipe CSVs"""
    if len(request.files) <= 0:
        resp = jsonify({"message": "No files where sent."})
        resp.status_code = 400
        return resp

    file_service = FileService()

    for rf in list(request.files.lists()):
        csv_merger = CsvMerger()
        # Validate and Sanitize Filename
        file_group_name: str = InputSanitizerService.sanitize_group_name(rf[0].lower())

        files: List[FileStorage] = rf[1]

        csv_merger.merge_csvs(files)
        # filepath ./temp/ecorp-bank-1905948329.csv
        filepath = csv_merger.get_merged_csvs(file_group_name)

        file_service.add_file_details(filepath, file_group_name)

    response_filepath = file_service.get_consolidated_filepath()

    filepaths = file_service.get_filepaths()
    # TODO: Move theis functionality into the above method
    # Adds zip files to filepaths
    if response_filepath not in filepaths:
        filepaths.append(response_filepath)

    _remove_files_after_request(filepaths)

    logger.info("Completed merging files")
    return send_file(response_filepath, as_attachment=True)


def _remove_files_after_request(filepaths):
    @after_this_request
    def remove_file(response):
        for filepath in filepaths:
            logger.info(f"Removing uploaded files for endpoint {filepath}")
            try:
                os.remove(filepath)
            except FileNotFoundError as e:
                errMsg = f"Unable to find file: {filepath}. {e}"
                logger.error(errMsg)
            except OSError as e:
                errMsg = f"Filename provided is a directory: {filepath}. {e}"
                logger.critical(errMsg)
                raise e
            except Exception as e:
                errMsg = f"An unknown exception occurred while removing {filepath}"
                logger.critical(errMsg)
                raise e

        return response


if __name__ == "__main__":
    app.run()
