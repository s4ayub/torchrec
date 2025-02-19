#!/usr/bin/env python3
# Copyright (c) Facebook, Inc. and its affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

import os
import tempfile
import unittest

import numpy as np
from torchrec.datasets.criteo import INT_FEATURE_COUNT, CAT_FEATURE_COUNT
from torchrec.datasets.scripts.preprocess_criteo import main
from torchrec.datasets.tests.criteo_test_utils import CriteoTest


class MainTest(unittest.TestCase):
    def test_main(self) -> None:
        num_rows = 10
        name = "day_0"
        with CriteoTest._create_dataset_tsv(
            num_rows=num_rows,
            filename=name,
        ) as in_file_path, tempfile.TemporaryDirectory() as output_dir:
            main(
                [
                    "--input_dir",
                    os.path.dirname(in_file_path),
                    "--output_dir",
                    output_dir,
                ]
            )

            dense = np.load(os.path.join(output_dir, name + "_dense.npy"))
            sparse = np.load(os.path.join(output_dir, name + "_sparse.npy"))
            labels = np.load(os.path.join(output_dir, name + "_labels.npy"))

            self.assertEqual(dense.shape, (num_rows, INT_FEATURE_COUNT))
            self.assertEqual(sparse.shape, (num_rows, CAT_FEATURE_COUNT))
            self.assertEqual(labels.shape, (num_rows, 1))
