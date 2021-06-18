# -*- coding:utf-8 -*-

import dgl
import torch as th
import torch.nn as nn
from base_model.layers import AtomEmbedding, Interaction, ShiftSoftplus, RBFLayer
from torch.nn.modules import PairwiseDistance


class SchNetModel(nn.Module):
    """
    SchNet Model from:
        Schütt, Kristof, et al.
        SchNet: A continuous-filter convolutional neural network
        for modeling quantum interactions. (NIPS'2017)
    """
    def __init__(self,
                 dim=64,
                 cutoff=5.0,
                 output_dim=1,
                 width=1,
                 n_conv=3,
                 norm=False,
                 atom_ref=None,
                 pre_train=None,
                 device='cpu'):
        """
        Args:
            dim: dimension of features
            output_dim: dimension of prediction
            cutoff: radius cutoff
            width: width in the RBF function
            n_conv: number of interaction layers
            atom_ref: used as the initial value of atom embeddings,
                      or set to None with random initialization
            norm: normalization
            device: cpu or gpu with idx
        """
        super(SchNetModel, self).__init__()
        self.name = "SchNet"
        self._dim = dim
        self.cutoff = cutoff
        self.width = width
        self.n_conv = n_conv
        self.atom_ref = atom_ref
        self.norm = norm
        self.activation = ShiftSoftplus()
        self.device = device

        if atom_ref is not None:
            self.e0 = AtomEmbedding(1, pre_train=atom_ref, device=self.device)
        if pre_train is None:
            self.embedding_layer = AtomEmbedding(dim, device=self.device)
        else:
            self.embedding_layer = AtomEmbedding(pre_train=pre_train,
                                                 device=self.device)
        self.rbf_layer = RBFLayer(0, cutoff, width, device=self.device)
        self.conv_layers = nn.ModuleList(
            [Interaction(self.rbf_layer._fan_out, dim) for i in range(n_conv)])

        self.atom_dense_layer1 = nn.Linear(dim, 64)
        self.atom_dense_layer2 = nn.Linear(64, output_dim)

    def set_mean_std(self, mean, std):
        self.mean_per_atom = th.tensor(mean, device=self.device)
        self.std_per_atom = th.tensor(std, device=self.device)

    def forward(self, mol_list):
        # g_list list of molecules

        g = dgl.batch([mol.ful_g for mol in mol_list])
        g.edata['distance'] = g.edata['distance'].reshape(-1, 1)
        g.to(self.device)

        self.embedding_layer(g)
        if self.atom_ref is not None:
            self.e0(g, "e0")
        self.rbf_layer(g)
        for idx in range(self.n_conv):
            self.conv_layers[idx](g)

        atom = self.atom_dense_layer1(g.ndata["node"])
        atom = self.activation(atom)
        res = self.atom_dense_layer2(atom)
        g.ndata["res"] = res

        if self.atom_ref is not None:
            g.ndata["res"] = g.ndata["res"] + g.ndata["e0"]

        if self.norm:
            g.ndata["res"] = g.ndata[
                "res"] * self.std_per_atom + self.mean_per_atom
        res = dgl.mean_nodes(g, "res")
        return res


if __name__ == "__main__":
    g = dgl.DGLGraph()
    g.add_nodes(2)
    g.add_edges([0, 0, 1, 1], [1, 0, 1, 0])
    g.edata["distance"] = th.tensor([1.0, 3.0, 2.0, 4.0]).reshape(-1, 1)
    g.ndata["node_type"] = th.LongTensor([1, 2])
    model = SchNetModel(dim=2)
    atom = model(g)
    print(atom)
