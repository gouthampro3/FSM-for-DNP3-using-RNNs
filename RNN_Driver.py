import torch
import torch.optim as optim
from random import shuffle

from aalpy.learning_algs import run_Lstar
from aalpy.oracles import RandomWordEqOracle
from aalpy.utils import load_automaton_from_file

from RNN import get_model, Optimization
from util import conformance_test, RNNSul

from extract_dnp3 import *
from automata_data_generation import AutomatonDataset

exp_name = 'dnp3'
device = None

num_training_samples = 400
num_val_samples = 155

automaton_data, input_al, output_al = generate_dnp3_data('captures-sample')

shuffle(automaton_data)
training_data, validation_data = automaton_data[:num_training_samples], automaton_data[num_training_samples:]
batch_size = 64
data_handler = AutomatonDataset(input_al, output_al, batch_size, device=device)
train, val = data_handler.create_dataset(training_data), data_handler.create_dataset(validation_data)

# Setup RNN parameters
model_type = 'gru'
activation_fun = 'relu'  # note that activation_fun value is irrelevant for GRU and LSTM
input_dim = len(input_al)
output_dim = len(output_al)
hidden_dim = 20
layer_dim = 2
dropout = 0  # 0.1 if layer_dim > 1 else 0
n_epochs = 100
optimizer = optim.Adam
learning_rate = 0.0005
weight_decay = 1e-6
early_stop = True  # Stop training if loss is smaller than small threshold for few epochs

model_params = {'input_dim': input_dim,
                'hidden_dim': hidden_dim,
                'layer_dim': layer_dim,
                'output_dim': output_dim,
                'nonlinearity': activation_fun,
                'dropout_prob': dropout,
                'data_handler': data_handler,
                'device': None}

model = get_model(model_type, model_params)

optimizer = optimizer(model.parameters(), lr=learning_rate, weight_decay=weight_decay)

opt = Optimization(model=model, optimizer=optimizer, device=None)

process_hs_fun = 'flatten_lstm' if model_type == 'lstm' else 'flatten'

# This will train the RNN
# If trained model with same parametrization exists, it will be loaded unless load flag is set to False
opt.train(train, val, n_epochs=n_epochs, exp_name=exp_name, early_stop=early_stop, save=True, load=True)

# disable all gradient computations to speed up execution
torch.no_grad()

# wrap RNN in AALpy's SUL interface
sul = RNNSul(model)
# this is a weak eq. oracle with weak configuration
eq_oracle = RandomWordEqOracle(input_al, sul, num_walks=1000, max_walk_len=10)

learned_model = run_Lstar(input_al, sul, eq_oracle, 'mealy')
learned_model.visualize()