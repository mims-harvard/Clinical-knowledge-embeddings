import dgl 
import torch 
import gc
import pandas as pd 
import pickle 
import pytorch_lightning as pl
import random
from model import EdgePredModel
from dataloader import edge_pred_dataloader
#from original import EdgePredModel, edge_pred_dataloader

# set seeds
torch.manual_seed(0)
import random
random.seed(0)
import numpy as np
np.random.seed(0)

from pytorch_lightning.loggers import WandbLogger

def open_pickle(f):
    with open(f, 'rb') as fname:
        node_dict = pickle.load(fname)
    return node_dict

def to_pickle(node_dict, f):
    with open(f, 'wb') as fname:
        pickle.dump(node_dict, fname)


device = "cuda"

def main():

    #
    # Set up model params
    #
    #homo_hg = dgl.load_graphs("new_homo_hg.pt") 
    homo_hg = dgl.load_graphs("/n/home01/ruthjohnson/kg_paper/construct_kg/phekg/new_homo_hg_hms.pt")
    homo_hg = homo_hg[0][0]
    
    n_epochs=5
    wandb_logger = WandbLogger()

    """
    trainer = pl.Trainer(max_epochs=n_epochs,
                        log_every_n_steps=1,
                        precision="bf16-mixed",
                        accelerator='gpu',
                        logger=wandb_logger)

    data_module = edge_pred_dataloader(homo_hg=homo_hg, 
                                    e_batch_size=500, 
                                    e_sampler=dgl.dataloading.MultiLayerNeighborSampler(
                                        [100, 10], prob='p'), e_n_neg=10)

    in_features = 1024
    hidden_features_1 = 512
    out_features = 128

    model = EdgePredModel(homo_hg, in_features, hidden_features_1, out_features)

    trainer.fit(model=model, datamodule=data_module)

    torch.save(model.het_gnn.state_dict(), "hgt_model_mini_edge.pt")

    """
    # {'train_loop_config': {'num_layers': 4, 'n_neg': 3, 
    # 'batch_size': 500, 'sampler_n': 15, 'lr': 0.0001, 
    # 'in_feat': 128, 'out_feat': 128, 'head_size': 512, 
    # 'num_heads': 3, 'dropout': 0}}

    config = {
        'num_layers': 4,
        'n_neg': 3,
        'batch_size': 500,
        'sampler_n': 15,
        'lr': 1e-4,
        'in_feat': 128,
        'out_feat': 128,
        'head_size': 512,
        'num_heads': 3, 
        'dropout': 0.0
    }
    
    #
    # Set up trainer
    # 
    wandb_logger = WandbLogger()

    trainer = pl.Trainer(max_epochs=n_epochs,
                        log_every_n_steps=10,
                        precision="bf16-mixed",
                        accelerator=device,
                        logger=wandb_logger)

    data_module = edge_pred_dataloader(homo_hg=homo_hg, homo_hg_dict=config)

    model = EdgePredModel(homo_hg, hgt_config=config)
    print(model)
    # train!
    trainer.fit(model=model, datamodule=data_module)

    #
    # Save trained model and weights
    #
    torch.save(model.het_gnn.state_dict(), "trained_hgt_mdl_hms.pt")


if __name__ == "__main__":
    main()


# srun python  ...
