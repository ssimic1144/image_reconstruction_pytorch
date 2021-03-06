import torch
import torch.nn as nn
import torch.nn.functional as F

class FourInputNet(nn.Module):
    def __init__(self):
        super(FourInputNet, self).__init__()

        conv_kernel = (3,3)
        conv_stride = (1,1)
        conv_padding = 1

        self.leaky_relu = nn.LeakyReLU()

        self.conv64 = self._conv_module(4, 64, conv_kernel, conv_stride, conv_padding,self.leaky_relu)
        self.conv128 = self._conv_module(64, 32, conv_kernel, conv_stride, conv_padding,self.leaky_relu)

        self.end_layer = self._exit_layer(32,1,conv_kernel,conv_stride,conv_padding,self.leaky_relu)




    def forward(self,one_image, three_image, five_image, seven_image):
        x = torch.cat((one_image,three_image,five_image,seven_image), dim=1)

        x = self.conv64(x)
        x = self.conv128(x)
        x = self.end_layer(x)

        return x 

    def _conv_module(self, in_channels, out_channels, kernel, stride, padding, leaky_relu):
        return nn.Sequential(
            nn.Conv2d(in_channels, in_channels, kernel, stride, padding), leaky_relu,
            nn.Conv2d(in_channels, in_channels, kernel, stride, padding), leaky_relu,
            nn.Conv2d(in_channels, out_channels, kernel, stride, padding), leaky_relu,
        )
    
    def _exit_layer(self,in_channels, out_channels,kernel,stride,padding,leaky_relu):
        return nn.Sequential(
            nn.Conv2d(in_channels,in_channels, kernel,stride,padding),leaky_relu,
            nn.Conv2d(in_channels,in_channels, kernel,stride,padding),leaky_relu,
            nn.Conv2d(in_channels,out_channels, kernel,stride,padding),leaky_relu,
            nn.Conv2d(out_channels,out_channels, kernel,stride,padding)
        )
