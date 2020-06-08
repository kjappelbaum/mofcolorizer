# MOFcolorizer

![image](static/logo.png)
Dash app that uses ML to predict the color of MOFs.

The current implementation uses a gradient boosted decision tree with quantile loss and RACs together with additional descriptors of the linkers as features.

The original model was trained using features derived from linker SMILES that we extracted using the MOFid code. As this can be done with the molsimplify code, we change this part in a future release (but keep an initial implementation with MOFid for consistency reasons, as we didn't test that the SMILES are identical between MOFid and molsimplify).
