import numpy as np
from copy import deepcopy

import PIL
from PIL import Image
import streamlit as st

import torch
import torch.nn.functional as F
from torchvision import models
from torchvision import transforms

def style_transfer(img_content, img_style, progress_bar, style_weight = 10000000, n_iters = 1):
    
    img_style = img_style.resize((224, 224), Image.ANTIALIAS)


    content_height, content_width = img_content.size[0], img_content.size[1]
    img_content = img_content.resize((224, 224), Image.ANTIALIAS)

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    def to_tensor(img):
        transform = transforms.ToTensor()
        return transform(img)[None]

    def to_image(tensor):
        img = tensor[0].detach().cpu().numpy()
        img = img.transpose(1, 2, 0)
        return np.clip(img, 0, 1)

    style_tensor = to_tensor(img_style).to(device).float()
    content_tensor = to_tensor(img_content).to(device).float()

    model = models.vgg16_bn(pretrained=True).to(device)
    model.eval()

    class ForwardHooks:
        def __init__(self):
            self.activation_dict = {}
        
        def get_hook(self, name):
            def hook(model, input, output):
                nonlocal self
                self.activation_dict[name] = output
            return hook

    def content_loss_fn(activations1, activations2):
        return F.mse_loss(activations1, activations2)

    def build_gramm_matrix(activation):
        _, c, w, h = activation.size()
        features = activation.view(c, w*h)
        G = torch.mm(features, features.t())
        return G.div(c * w * h)

    def style_loss_fn(activations1, gramm_matix2):
        gramm_matix1 = build_gramm_matrix(activations1)
        return F.mse_loss(gramm_matix1, gramm_matix2)

    def get_activations(inputs, hooks, activation_names):
        return [hooks.activation_dict[feature_name] for feature_name in activation_names]

    hooks = ForwardHooks()
    for name, module in model.named_modules():
        module.register_forward_hook(hooks.get_hook(name))

    content_activation_names = ['features.10']
    style_activation_names = ['features.0', 'features.3', 'features.7', 'features.10', 'features.14']

    with torch.no_grad():
        model(content_tensor)
        content_target_activations = get_activations(content_tensor, hooks, content_activation_names)

        model(style_tensor)
        style_target_activations = get_activations(style_tensor, hooks, style_activation_names)
        
        style_target_gramm_matrixes = [
            build_gramm_matrix(activation) for activation in style_target_activations
        ]

    for param in model.parameters():
        param.requires_grad = False
    
    optimization_tensor = content_tensor.clone().contiguous()
    optimization_tensor.requires_grad=True
    optimizer = torch.optim.LBFGS([optimization_tensor])

    content_weight = 1 #frozen hyperparameter

    for i in range(n_iters):
        def closure():
            optimizer.zero_grad()
            model(optimization_tensor)

            content_activations = get_activations(optimization_tensor, hooks, content_activation_names)
            style_activations = get_activations(optimization_tensor, hooks, style_activation_names)

            content_losses = [
                content_loss_fn(activation1, activation2)
                for activation1, activation2 in zip(content_activations, content_target_activations)
            ]
            content_loss = sum(content_losses) * content_weight
                
            style_losses = [
                style_loss_fn(activation1, gramm2)
                for activation1, gramm2 in zip(style_activations, style_target_gramm_matrixes)
            ]
            style_loss = sum(style_losses) * style_weight

            loss = content_loss + style_loss
                    
            loss.backward()

            return loss
        
        optimizer.step(closure)

        progress_bar.progress((i + 1) / n_iters)

    opt_tensor_numpy = optimization_tensor[0].cpu().detach().numpy()
    pil_image = Image.fromarray(np.array(np.clip(opt_tensor_numpy.transpose(1, 2, 0), 0, 1) * 255, dtype=np.uint8))
    resized = pil_image.resize((content_height, content_width), Image.Resampling.BICUBIC)

    return resized
