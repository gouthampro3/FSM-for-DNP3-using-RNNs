import random
from collections import defaultdict
from itertools import product

import torch
from aalpy.automata import MealyMachine
from aalpy.utils import load_automaton_from_file

class AutomatonDataset:
    def __init__(self, input_al_str, classes, batch_size, device=None):
        self.inputs = input_al_str
        self.classes = [str(c) for c in classes]
        self.class_to_index = {k: ind for ind, k in enumerate(classes)}
        self.index_to_class = {ind: k for ind, k in enumerate(classes)}
        self.len_dict = defaultdict(list)
        self.batch_size = batch_size
        if device is None:
            self.device = torch.device('cuda:0' if device != 'cpu' and torch.cuda.is_available() else "cpu")
        else:
            self.device = device

    def input_tensor(self, line, length):
        tensor = torch.zeros(length, len(self.inputs)).to(self.device)
        for i, el in enumerate(line):
            tensor[i][self.inputs.index(el)] = 1
        return tensor

    def classification_tensor(self, classification):
        return torch.LongTensor([self.class_to_index[classification]]).to(self.device)

    def create_dataset(self, data):
        batches = []
        for d in data:
            self.len_dict[len(d[0])].append(d)

        for _, seqs in self.len_dict.items():
            sequences = []
            labels = []
            for s in seqs:
                sequences.append(self.input_tensor(s[0], len(s[0])))
                labels.append(self.classification_tensor(s[1]))

            # experimental
            if len(sequences) < self.batch_size:
                while len(sequences) < self.batch_size:
                    sequences.extend(sequences)
                    labels.extend(labels)
                sequences = sequences[:self.batch_size]
                labels = labels[:self.batch_size]

            for i in range(0, len(sequences), self.batch_size):
                batch_seqs = torch.stack(sequences[i:i + self.batch_size])
                batch_labels = torch.stack(labels[i:i + self.batch_size])

                batches.append((batch_seqs, batch_labels))

        return batches
