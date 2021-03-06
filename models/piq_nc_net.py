import torch
import torch.nn as nn
import torch.nn.functional as F

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()

        conv_kernel = (3,3)
        conv_stride = (1,1)
        conv_padding = 1

        self.sigmoid = nn.Sigmoid()
        self.tanh = nn.Tanh()
        self.elu = nn.ELU()
        
        self.conv32 = self._conv_module(2, 32, conv_kernel, conv_stride, conv_padding,self.elu)
        self.conv32x32 = self._conv_module(32, 32, conv_kernel, conv_stride, conv_padding,self.tanh)
        self.end_layer = self._exit_layer(32,1,conv_kernel,conv_stride,conv_padding,self.elu)




    def forward(self,prev_img, next_img):
        x = torch.cat((prev_img,next_img), dim=1)

        x = self.conv32(x)
        x = self.conv32x32(x)
        x = self.end_layer(x)
        x = self.sigmoid(x)
        return x 

    def _conv_module(self, in_channels, out_channels, kernel, stride, padding, activation):
        return nn.Sequential(
            nn.Conv2d(in_channels, in_channels, kernel, stride, padding), activation,
            nn.Conv2d(in_channels, out_channels, kernel, stride, padding), activation,
        )
    
    def _exit_layer(self,in_channels, out_channels,kernel,stride,padding,activation):
        return nn.Sequential(
            nn.Conv2d(in_channels,in_channels, kernel,stride,padding),activation,
            nn.Conv2d(in_channels,out_channels, kernel,stride,padding),activation,
            nn.Conv2d(out_channels,out_channels, kernel,stride,padding)
        )
