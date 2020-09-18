from builtins import range
import numpy as np



def affine_forward(x, w, b):
    """
    Computes the forward pass for an affine (fully-connected) layer.

    The input x has shape (N, d_1, ..., d_k) and contains a minibatch of N
    examples, where each example x[i] has shape (d_1, ..., d_k). We will
    reshape each input into a vector of dimension D = d_1 * ... * d_k, and
    then transform it to an output vector of dimension M.

    Inputs:
    - x: A numpy array containing input data, of shape (N, d_1, ..., d_k)
    - w: A numpy array of weights, of shape (D, M)
    - b: A numpy array of biases, of shape (M,)

    Returns a tuple of:
    - out: output, of shape (N, M)
    - cache: (x, w, b)
    """
    out = None
    ###########################################################################
    # TODO: Implement the affine forward pass. Store the result in out. You   #
    # will need to reshape the input into rows.                               #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    #print(x.shape)
    #print(type(x))
    #print(x.shape,"virginX shape")
    N=x.shape[0]
    D=(int)(np.prod(x.shape)/N)
    reshapedX=x.reshape((N,D))

    #dummy=np.matmul(reshapedX,w)
    #print(reshapedX.shape,"reshapedX")
    #print(dummy.shape,"dummy")
    #print(w.shape,"w")
    b= np.squeeze(b)
    #print(b.shape,"b")
    
    #print(reshapedX.shape,"reshapedX")
    #print(w.shape,"w")
    out=np.matmul(reshapedX,w)+b
    
    pass
    #print("in forward :::: ")
    #print(x.shape,"x")
    #print(w.shape,"w")
    #print(b.shape,"b")
    #print(out.shape,"result")
    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    cache = (x, w, b)
    return out, cache


def affine_backward(dout, cache):
    """
    Computes the backward pass for an affine layer.

    Inputs:
    - dout: Upstream derivative, of shape (N, M)
    - cache: Tuple of:
      - x: Input data, of shape (N, d_1, ... d_k)
      - w: Weights, of shape (D, M)
      - b: Biases, of shape (M,)

    Returns a tuple of:
    - dx: Gradient with respect to x, of shape (N, d1, ..., d_k)
    - dw: Gradient with respect to w, of shape (D, M)
    - db: Gradient with respect to b, of shape (M,)
    """
    x, w, b = cache
    dx, dw, db = None, None, None
    ###########################################################################
    # TODO: Implement the affine backward pass.                               #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    N=x.shape[0]
    D=(int)(np.prod(x.shape)/N)
    reshapedX=x.reshape((N,D))

    #A=reshapedX.transpose()
    #print(A.shape,"A")
    #print(dout.shape,"dout")
    dw=np.matmul(reshapedX.transpose(),dout)
    dx=np.matmul(dout,w.transpose())
    db=np.sum(dout.transpose(),axis=1)
    dx=dx.reshape((x.shape))

    pass

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return dx, dw, db


def relu_forward(x):
    """
    Computes the forward pass for a layer of rectified linear units (ReLUs).

    Input:
    - x: Inputs, of any shape

    Returns a tuple of:
    - out: Output, of the same shape as x
    - cache: x
    """
    out = None
    ###########################################################################
    # TODO: Implement the ReLU forward pass.                                  #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    out=x*(x>0)
    pass

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    cache = x
    return out, cache


def relu_backward(dout, cache):
    """
    Computes the backward pass for a layer of rectified linear units (ReLUs).

    Input:
    - dout: Upstream derivatives, of any shape
    - cache: Input x, of same shape as dout

    Returns:
    - dx: Gradient with respect to x
    """
    dx, x = None, cache
    ###########################################################################
    # TODO: Implement the ReLU backward pass.                                 #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    binary=np.zeros_like(x)
    binary[x > 0] = 1
    #print(x)
    dx=np.multiply(dout,binary)
    #print(dx)
    pass

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return dx



def batchnorm_forward(x, gamma, beta, bn_param):
    """
    Forward pass for batch normalization.

    During training the sample mean and (uncorrected) sample variance are
    computed from minibatch statistics and used to normalize the incoming data.
    During training we also keep an exponentially decaying running mean of the
    mean and variance of each feature, and these averages are used to normalize
    data at test-time.

    At each timestep we update the running averages for mean and variance using
    an exponential decay based on the momentum parameter:

    running_mean = momentum * running_mean + (1 - momentum) * sample_mean
    running_var = momentum * running_var + (1 - momentum) * sample_var

    Note that the batch normalization paper suggests a different test-time
    behavior: they compute sample mean and variance for each feature using a
    large number of training images rather than using a running average. For
    this implementation we have chosen to use running averages instead since
    they do not require an additional estimation step; the torch7
    implementation of batch normalization also uses running averages.

    Input:
    - x: Data of shape (N, D)
    - gamma: Scale parameter of shape (D,)
    - beta: Shift paremeter of shape (D,)
    - bn_param: Dictionary with the following keys:
      - mode: 'train' or 'test'; required
      - eps: Constant for numeric stability
      - momentum: Constant for running mean / variance.
      - running_mean: Array of shape (D,) giving running mean of features
      - running_var Array of shape (D,) giving running variance of features

    Returns a tuple of:
    - out: of shape (N, D)
    - cache: A tuple of values needed in the backward pass
    """

   # print(bn_param.keys())
    mode = bn_param["mode"]
    eps = bn_param.get("eps", 1e-5)

   

    if(mode != "none"):
      #print(x.shape,"b f shape")
      N, D = x.shape
      momentum = bn_param.get("momentum", 0.9) 
      running_mean = bn_param.get("running_mean", np.zeros((D,)))
      running_var = bn_param.get("running_var", np.zeros((D,)))
    
  

    out, cache = None, None
    if mode == "train" or mode=='none':
        #######################################################################
        # TODO: Implement the training-time forward pass for batch norm.      #
        # Use minibatch statistics to compute the mean and variance, use      #
        # these statistics to normalize the incoming data, and scale and      #
        # shift the normalized data using gamma and beta.                     #
        #                                                                     #
        # You should store the output in the variable out. Any intermediates  #
        # that you need for the backward pass should be stored in the cache   #
        # variable.                                                           #
        #                                                                     #
        # You should also use your computed sample mean and variance together #
        # with the momentum variable to update the running mean and running   #
        # variance, storing your result in the running_mean and running_var   #
        # variables.                                                          #
        #                                                                     #
        # Note that though you should be keeping track of the running         #
        # variance, you should normalize the data based on the standard       #
        # deviation (square root of variance) instead!                        #
        # Referencing the original paper (https://arxiv.org/abs/1502.03167)   #
        # might prove to be helpful.                                          #
        #######################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
       # print(x.shape)
        sample_mean=np.mean(x,axis=0)
        sample_var=np.var(x,axis=0)
       # print(sample_mean.shape,"mean")
       # print(sample_var.shape,"var")


       
        if mode != 'none' :
          running_mean = momentum * running_mean + (1 - momentum) * sample_mean
          running_var = momentum * running_var + (1 - momentum) * sample_var

        #print(running_mean.shape,"mean")
        #print(running_var.shape,"var")

        out= (x-sample_mean)/np.sqrt(sample_var+eps)
        cache=out,sample_var,eps,gamma,sample_mean,x
        out=gamma*out+beta


    




        pass

        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        #######################################################################
        #                           END OF YOUR CODE                          #
        #######################################################################
    elif mode == "test":
        #######################################################################
        # TODO: Implement the test-time forward pass for batch normalization. #
        # Use the running mean and variance to normalize the incoming data,   #
        # then scale and shift the normalized data using gamma and beta.      #
        # Store the result in the out variable.                               #
        #######################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        out= (x-running_mean)/np.sqrt(running_var+eps)
        out = out *gamma + beta
        
        pass

        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        #######################################################################
        #                          END OF YOUR CODE                           #
        #######################################################################
    else:
        raise ValueError('Invalid forward batchnorm mode "%s"' % mode)

    # Store the updated running means back into bn_param
    if mode != 'none':
      bn_param["running_mean"] = running_mean
      bn_param["running_var"] = running_var

    return out, cache



def batchnorm_backward(dout, cache):
    """
    Backward pass for batch normalization.

    For this implementation, you should write out a computation graph for
    batch normalization on paper and propagate gradients backward through
    intermediate nodes.

    Inputs:
    - dout: Upstream derivatives, of shape (N, D)
    - cache: Variable of intermediates from batchnorm_forward.

    Returns a tuple of:
    - dx: Gradient with respect to inputs x, of shape (N, D)
    - dgamma: Gradient with respect to scale parameter gamma, of shape (D,)
    - dbeta: Gradient with respect to shift parameter beta, of shape (D,)
    """
    dx, dgamma, dbeta = None, None, None
    ###########################################################################
    # TODO: Implement the backward pass for batch normalization. Store the    #
    # results in the dx, dgamma, and dbeta variables.                         #
    # Referencing the original paper (https://arxiv.org/abs/1502.03167)       #
    # might prove to be helpful.                                              #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    xbar,var,epsilon,gamma,mean,x=cache

    #print(x.shape,"x")
    #print(dout.shape,"dout")

    #gamma=gamma.reshape((1,gamma.shape[0]))

    dxbar=dout*gamma
    dx=dxbar/np.sqrt(epsilon+var)
    dgamma=np.sum(np.multiply(dout,xbar),axis=0)
    dbeta=np.sum(dout,axis=0)
    
    dsigma2=np.sum(np.multiply(x-mean,dxbar),axis=0)*(-0.5)*((var+epsilon)**(-1.5))
    #A=np.sum(np.multiply(x-mean,dxbar),axis=0)

    
    #dsigma2=A*(-0.5)*((var+expression)**(-1.5))




    dmu=np.sum(dxbar*(-1)/np.sqrt(var+epsilon),axis=0)+dsigma2*np.mean(-2*(x-mean),axis=0)
    dx=dx+dsigma2*2*(x-mean)/dout.shape[0]+dmu/dout.shape[0]

    pass

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################

    return dx, dgamma, dbeta


def batchnorm_backward_alt(dout, cache):
    """
    Alternative backward pass for batch normalization.

    For this implementation you should work out the derivatives for the batch
    normalizaton backward pass on paper and simplify as much as possible. You
    should be able to derive a simple expression for the backward pass. 
    See the jupyter notebook for more hints.
     
    Note: This implementation should expect to receive the same cache variable
    as batchnorm_backward, but might not use all of the values in the cache.

    Inputs / outputs: Same as batchnorm_backward
    """
    dx, dgamma, dbeta = None, None, None
    ###########################################################################
    # TODO: Implement the backward pass for batch normalization. Store the    #
    # results in the dx, dgamma, and dbeta variables.                         #
    #                                                                         #
    # After computing the gradient with respect to the centered inputs, you   #
    # should be able to compute gradients with respect to the inputs in a     #
    # single statement; our implementation fits on a single 80-character line.#
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    #refrencing https://arxiv.org/pdf/1502.03167.pdf
   
    xbar,var,epsilon,gamma,mean,x=cache

    pass
    dbeta=np.sum(dout,axis=0)
    dgamma=np.sum(np.multiply(xbar,dout),axis=0)
    x_norm=xbar
    x_mu=x-mean
    var_inv=1/np.sqrt(var+epsilon)
    

    N = dout.shape[0]

    dgamma = np.sum(dout * x_norm, axis=0)
    dbeta = np.sum(dout, axis=0)

    dvar = np.sum(dout * gamma * x_mu, axis=0) * -0.5 * (var_inv ** 3)
    dmu = np.sum(dout * gamma * -var_inv, axis=0) + dvar * -2 * np.mean(x_mu, axis=0)

    dx = dout * gamma * var_inv + dvar * (2 / N) * x_mu + dmu * (1 / N)
 

    


    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################

    return dx, dgamma, dbeta


def layernorm_forward(x, gamma, beta, ln_param):
    """
    Forward pass for layer normalization.

    During both training and test-time, the incoming data is normalized per data-point,
    before being scaled by gamma and beta parameters identical to that of batch normalization.
    
    Note that in contrast to batch normalization, the behavior during train and test-time for
    layer normalization are identical, and we do not need to keep track of running averages
    of any sort.

    Input:
    - x: Data of shape (N, D)
    - gamma: Scale parameter of shape (D,)
    - beta: Shift paremeter of shape (D,)
    - ln_param: Dictionary with the following keys:
        - eps: Constant for numeric stability

    Returns a tuple of:
    - out: of shape (N, D)
    - cache: A tuple of values needed in the backward pass
    """
    out, cache = None, None
    eps = ln_param.get("eps", 1e-5)
    ###########################################################################
    # TODO: Implement the training-time forward pass for layer norm.          #
    # Normalize the incoming data, and scale and  shift the normalized data   #
    #  using gamma and beta.                                                  #
    # HINT: this can be done by slightly modifying your training-time         #
    # implementation of  batch normalization, and inserting a line or two of  #
    # well-placed code. In particular, can you think of any matrix            #
    # transformations you could perform, that would enable you to copy over   #
    # the batch norm code and leave it almost unchanged?                      #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    
    """
    sample_mean=np.mean(x,axis=1,keepdims=True)
    sample_var=np.var(x,axis=1,keepdims=True)

    print(x.shape,"x")
    print(sample_var.shape,"var and mean")
    print(gamma.shape,"gamma and beta")




    out= (x-sample_mean)/np.sqrt(sample_var+eps)

    print(out)


    cache=out,sample_var,eps,gamma,sample_mean,x

    out=gamma*out+beta
    """
    
    dic={}
    dic['mode']='none'

   # print("im going to call batch for")
   
    temp=x.transpose()
    gamma=gamma.reshape((gamma.shape[0],1))
    beta=beta.reshape((beta.shape[0],1))

    out,cache=batchnorm_forward(temp,gamma,beta,dic)
    out=out.transpose()
    #def batchnorm_forward(x, gamma, beta, bn_param):
    

    



   
  

    pass

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return out, cache


def layernorm_backward(dout, cache):
    """
    Backward pass for layer normalization.

    For this implementation, you can heavily rely on the work you've done already
    for batch normalization.

    Inputs:
    - dout: Upstream derivatives, of shape (N, D)
    - cache: Variable of intermediates from layernorm_forward.

    Returns a tuple of:
    - dx: Gradient with respect to inputs x, of shape (N, D)
    - dgamma: Gradient with respect to scale parameter gamma, of shape (D,)
    - dbeta: Gradient with respect to shift parameter beta, of shape (D,)
    """
    dx, dgamma, dbeta = None, None, None
    ###########################################################################
    # TODO: Implement the backward pass for layer norm.                       #
    #                                                                         #
    # HINT: this can be done by slightly modifying your training-time         #
    # implementation of batch normalization. The hints to the forward pass    #
    # still apply!                                                            #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    
    xbar,var,epsilon,gamma,mean,x=cache
    dx,dgamma,dbeta= batchnorm_backward(dout.transpose(),cache)
    dx=dx.transpose()

    xbar=xbar.transpose()

    gamma=gamma.reshape((gamma.shape[0]))
    dxbar=dout*gamma
 
    dgamma=np.sum(np.multiply(dout,xbar),axis=0)
    dbeta=np.sum(dout,axis=0)

    




    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return dx, dgamma, dbeta


def dropout_forward(x, dropout_param):
    """
    Performs the forward pass for (inverted) dropout.

    Inputs:
    - x: Input data, of any shape
    - dropout_param: A dictionary with the following keys:
      - p: Dropout parameter. We keep each neuron output with probability p.
      - mode: 'test' or 'train'. If the mode is train, then perform dropout;
        if the mode is test, then just return the input.
      - seed: Seed for the random number generator. Passing seed makes this
        function deterministic, which is needed for gradient checking but not
        in real networks.

    Outputs:
    - out: Array of the same shape as x.
    - cache: tuple (dropout_param, mask). In training mode, mask is the dropout
      mask that was used to multiply the input; in test mode, mask is None.

    NOTE: Please implement **inverted** dropout, not the vanilla version of dropout.
    See http://cs231n.github.io/neural-networks-2/#reg for more details.

    NOTE 2: Keep in mind that p is the probability of **keep** a neuron
    output; this might be contrary to some sources, where it is referred to
    as the probability of dropping a neuron output.
    """
    p, mode = dropout_param["p"], dropout_param["mode"]
    if "seed" in dropout_param:
        np.random.seed(dropout_param["seed"])

    mask = None
    out = None

    if mode == "train":
        #######################################################################
        # TODO: Implement training phase forward pass for inverted dropout.   #
        # Store the dropout mask in the mask variable.                        #
        #######################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        mask=np.random.uniform(low=0.0, high=1.0, size=x.shape)

        """
        print(type(mask))
        print(mask.shape)
        print(x.shape)
        """
       # print(mask)
        binary=np.zeros_like(x)

        
        binary[mask<= p] =1
        #print(binary)
        out=np.multiply(binary,x)/p
      

        pass

        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        #######################################################################
        #                           END OF YOUR CODE                          #
        #######################################################################
    elif mode == "test":
        #######################################################################
        # TODO: Implement the test phase forward pass for inverted dropout.   #
        #######################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        out=x
        binary=np.ones_like(x)
        pass

        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        #######################################################################
        #                            END OF YOUR CODE                         #
        #######################################################################

    cache = dropout_param, mask , binary
    out = out.astype(x.dtype, copy=False)

    return out, cache


def dropout_backward(dout, cache):
    """
    Perform the backward pass for (inverted) dropout.

    Inputs:
    - dout: Upstream derivatives, of any shape
    - cache: (dropout_param, mask) from dropout_forward.
    """
    dropout_param, mask , binary=cache
    mode = dropout_param["mode"]

    dx = None
    if mode == "train":
        #######################################################################
        # TODO: Implement training phase backward pass for inverted dropout   #
        #######################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        
        p=dropout_param['p']
        dx= np.multiply(dout,binary)/p
   
        pass

        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        #######################################################################
        #                          END OF YOUR CODE                           #
        #######################################################################
    elif mode == "test":
        dx = dout
    return dx


def conv_forward_naive(x, w, b, conv_param):
    """
    A naive implementation of the forward pass for a convolutional layer.

    The input consists of N data points, each with C channels, height H and
    width W. We convolve each input with F different filters, where each filter
    spans all C channels and has height HH and width WW.

    Input:
    - x: Input data of shape (N, C, H, W)
    - w: Filter weights of shape (F, C, HH, WW)
    - b: Biases, of shape (F,)
    - conv_param: A dictionary with the following keys:
      - 'stride': The number of pixels between adjacent receptive fields in the
        horizontal and vertical directions.
      - 'pad': The number of pixels that will be used to zero-pad the input. 
        

    During padding, 'pad' zeros should be placed symmetrically (i.e equally on both sides)
    along the height and width axes of the input. Be careful not to modfiy the original
    input x directly.

    Returns a tuple of:
    - out: Output data, of shape (N, F, H', W') where H' and W' are given by
      H' = 1 + (H + 2 * pad - HH) / stride
      W' = 1 + (W + 2 * pad - WW) / stride
    - cache: (x, w, b, conv_param)
    """
    out = None
    ###########################################################################
    # TODO: Implement the convolutional forward pass.                         #
    # Hint: you can use the function np.pad for padding.                      #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    H=x.shape[2]
    W=x.shape[3]
    HH=w.shape[2]
    WW=w.shape[3]
    pad=conv_param['pad']
    stride=conv_param['stride']
    pw=((0,0),(0,0),(pad,pad),(pad,pad))
    padded=np.pad(x, [(0,0), (0,0), (pad, pad), (pad, pad)])

    Hp = (int)(1 + (H + 2 * pad - HH) / stride)
    Wp = (int)(1 + (W + 2 * pad - WW) / stride)
    N=x.shape[0]
    F=w.shape[0]
    out=np.zeros((N,F,Hp,Wp))
    for n in range (N):
      


      for f in range (F):
        upperLeft=[0,0]
        
        for h in range (Hp):
          upperLeft[1]=0
          for www in range (Wp):
            A=w[f , : , : , : ]
            B=padded[ n , : , upperLeft[0]:upperLeft[0]+HH , upperLeft[1]:upperLeft[1]+WW ]
            C=A*B
            SUM=np.sum(C)
            out[n,f,h,www]=SUM+b[f]
            upperLeft[1]+=stride
          upperLeft[0]+=stride

   
    pass
   

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    cache = (x, w, b, conv_param)
    return out, cache






def conv_backward_naive(dout, cache):
    """
    A naive implementation of the backward pass for a convolutional layer.
    Inputs:
    - dout: Upstream derivatives.
    - cache: A tuple of (x, w, b, conv_param) as in conv_forward_naive
    Returns a tuple of:
    - dx: Gradient with respect to x
    - dw: Gradient with respect to w
    - db: Gradient with respect to b
    """
    dx, dw, db = None, None, None
    ###########################################################################
    # TODO: Implement the convolutional backward pass.                        #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    # Unpack cache
    x, w, _, conv_param = cache
    stride = conv_param['stride'] 
    pad = conv_param['pad']
    _, _, H, W = x.shape
    _, _, HH, WW = w.shape
    N, F, out_h, out_w = dout.shape

    x_pad = np.pad(x, [(0,0), (0,0), (pad, pad), (pad, pad)])
    dw = np.zeros(shape=w.shape)
    dx = np.zeros(shape=x.shape)
    dx_pad = np.pad(dx, [(0,0), (0,0), (pad, pad), (pad, pad)])
    
    db = np.sum(dout, axis=(0,2,3))
    for sample in range(N):
      for fil in range(F):
        for h in range(out_h):
          start_h = stride * h
          end_h = stride * h + HH
          for wi in range(out_w):
            start_w = stride * wi
            end_w = stride * wi + WW
            x_conv = x_pad[sample,:,start_h:end_h,start_w:end_w]
            dx_pad[sample,:,start_h:end_h,start_w:end_w] += dout[sample,fil,h,wi] * w[fil]
            dw[fil] += dout[sample,fil,h,wi] * x_conv
    
    dx = dx_pad[:,:,1:H+1,1:W+1]

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return dx, dw, db    


def max_pool_forward_naive(x, pool_param):
    """
    A naive implementation of the forward pass for a max-pooling layer.

    Inputs:
    - x: Input data, of shape (N, C, H, W)
    - pool_param: dictionary with the following keys:
      - 'pool_height': The height of each pooling region
      - 'pool_width': The width of each pooling region
      - 'stride': The distance between adjacent pooling regions

    No padding is necessary here. Output size is given by 

    Returns a tuple of:
    - out: Output data, of shape (N, C, H', W') where H' and W' are given by
      H' = 1 + (H - pool_height) / stride
      W' = 1 + (W - pool_width) / stride
    - cache: (x, pool_param)
    """
    out = None
    ###########################################################################
    # TODO: Implement the max-pooling forward pass                            #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    pool_height=pool_param['pool_height']
    pool_width=pool_param['pool_width']
    stride=pool_param['stride']


    N,C,H,W=x.shape
    Hp=(int) (1+(H-pool_height)/stride)
    Wp=(int) (1+(W-pool_width)/stride)

    out=np.zeros(shape=(N,C,Hp,Wp))

    for n in range (N):
      for c in range (C):
        upperLeft=[0,0]
        for h in range (Hp):
          upperLeft[1]=0
          for w in range (Wp):     
            window=x[ n , c , upperLeft[0] : upperLeft[0] + pool_height , upperLeft[1] : upperLeft[1] + pool_width]
            out[n][c][h][w]=np.max(window)
            upperLeft[1]+=stride
          upperLeft[0]+=stride

 
    pass

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    cache = (x, pool_param)
    return out, cache


def max_pool_backward_naive(dout, cache):
    """
    A naive implementation of the backward pass for a max-pooling layer.

    Inputs:
    - dout: Upstream derivatives
    - cache: A tuple of (x, pool_param) as in the forward pass.

    Returns:
    - dx: Gradient with respect to x
    """
    dx = None
    ###########################################################################
    # TODO: Implement the max-pooling backward pass                           #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    pass
    x,pool_param = cache
    pool_height=pool_param['pool_height']
    pool_width=pool_param['pool_width']
    stride=pool_param['stride']

    dx=np.zeros_like(x)

    N,C,H,W=x.shape
    Hp=dout.shape[2]
    Wp=dout.shape[3]
    

 


    for n in range (N):
      for c in range (C):
        upperLeft=[0,0]
        for h in range (Hp):
          upperLeft[1]=0
       
          for w in range (Wp):     
            window=x[ n , c , upperLeft[0] : upperLeft[0] + pool_height , upperLeft[1] : upperLeft[1] + pool_width]
            temp=np.argmax(window)

            hor=temp//pool_height
            ver=temp % pool_width


            hor=upperLeft[0]+hor
            ver=upperLeft[1]+ver

            dx[n][c][hor][ver]+=dout[n][c][h][w]
            

            upperLeft[1]+=stride
          upperLeft[0]+=stride

   



   
    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
   
    return dx


def spatial_batchnorm_forward(x, gamma, beta, bn_param):
    """
    Computes the forward pass for spatial batch normalization.

    Inputs:
    - x: Input data of shape (N, C, H, W)
    - gamma: Scale parameter, of shape (C,)
    - beta: Shift parameter, of shape (C,)
    - bn_param: Dictionary with the following keys:
      - mode: 'train' or 'test'; required
      - eps: Constant for numeric stability
      - momentum: Constant for running mean / variance. momentum=0 means that
        old information is discarded completely at every time step, while
        momentum=1 means that new information is never incorporated. The
        default of momentum=0.9 should work well in most situations.
      - running_mean: Array of shape (D,) giving running mean of features
      - running_var Array of shape (D,) giving running variance of features

    Returns a tuple of:
    - out: Output data, of shape (N, C, H, W)
    - cache: Values needed for the backward pass
    """
    out, cache = None, None

    ###########################################################################
    # TODO: Implement the forward pass for spatial batch normalization.       #
    #                                                                         #
    # HINT: You can implement spatial batch normalization by calling the      #
    # vanilla version of batch normalization you implemented above.           #
    # Your implementation should be very short; ours is less than five lines. #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    """
    mode=bn_param.get("mode")
    eps=bn_param.get("eps",1e-6)
    momentum=bn_param.get("momentum",0.9)
    running_mean=bn_param.get("running_mean",0)
    running_var=bn_param.get("running_var",0)
   

    N, C, H, W = x.shape
    mean = np.mean(x, axis = (0, 2, 3))
    var = np.var(x, axis=(0, 2, 3))
    xbar = (x - mean.reshape((1, C, 1, 1))) * 1.0 / np.sqrt(var.reshape((1, C, 1, 1)) + eps)
    out = gamma.reshape((1, C, 1, 1)) * xbar + beta.reshape((1, C, 1, 1))
    cache=(xbar,var,eps,gamma,mean,x)
    """
    N, C, H, W = x.shape
    x_=np.transpose(x,axes=(0,2,3,1))
    x_=x_.reshape((N*H*W,C))

    out,cache=batchnorm_forward(x_,gamma,beta,bn_param)
    out=out.reshape((N,H,W,C))
    out=np.transpose(out,axes=(0,3,1,2))
    #print(out.shape,"out")


    

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################

    return out, cache


def spatial_batchnorm_backward(dout, cache):
    """
    Computes the backward pass for spatial batch normalization.

    Inputs:
    - dout: Upstream derivatives, of shape (N, C, H, W)
    - cache: Values from the forward pass

    Returns a tuple of:
    - dx: Gradient with respect to inputs, of shape (N, C, H, W)
    - dgamma: Gradient with respect to scale parameter, of shape (C,)
    - dbeta: Gradient with respect to shift parameter, of shape (C,)
    """
    dx, dgamma, dbeta = None, None, None

    ###########################################################################
    # TODO: Implement the backward pass for spatial batch normalization.      #
    #                                                                         #
    # HINT: You can implement spatial batch normalization by calling the      #
    # vanilla version of batch normalization you implemented above.           #
    # Your implementation should be very short; ours is less than five lines. #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    N,C,H,W=dout.shape
    dout_=np.transpose(dout,axes=(0,2,3,1))
    dout_=dout_.reshape((-1,C))
    

    dx,dgamma,dbeta=batchnorm_backward(dout_,cache)
    dx=dx.reshape((N,H,W,C))
    dx=np.transpose(dx,axes=(0,3,1,2))

    pass

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################

    return dx, dgamma, dbeta


def spatial_groupnorm_forward(x, gamma, beta, G, gn_param):
    """
    Computes the forward pass for spatial group normalization.
    In contrast to layer normalization, group normalization splits each entry 
    in the data into G contiguous pieces, which it then normalizes independently.
    Per feature shifting and scaling are then applied to the data, in a manner identical
    to that of batch normalization and layer normalization.

    Inputs:
    - x: Input data of shape (N, C, H, W)
    - gamma: Scale parameter, of shape (C,)
    - beta: Shift parameter, of shape (C,)
    - G: Integer mumber of groups to split into, should be a divisor of C
    - gn_param: Dictionary with the following keys:
      - eps: Constant for numeric stability

    Returns a tuple of:
    - out: Output data, of shape (N, C, H, W)
    - cache: Values needed for the backward pass
    """
    out, cache = None, None
    eps = gn_param.get("eps", 1e-5)
    ###########################################################################
    # TODO: Implement the forward pass for spatial group normalization.       #
    # This will be extremely similar to the layer norm implementation.        #
    # In particular, think about how you could transform the matrix so that   #
    # the bulk of the code is similar to both train-time batch normalization  #
    # and layer normalization!                                                #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
  
    x_=np.split(x,G,axis=1)
    x_=np.stack( x_, axis=0 )

    N,C,H,W=x.shape
    out=np.zeros_like(x)

    """
    print(x.shape,"x")
   # print(type(x_))
   # print(len(x_),"len")
    print(C,"C")
    print(G,"G")
   # print(x_[0].shape,"0")
   # print(x_[1].shape,"1")
    print(x_.shape,"x_")
    print(gamma.shape,"gamma")
    """
    
    gamma_=np.split(gamma,G,axis=1)
    gamma_=np.stack( gamma_, axis=0 )

    beta_=np.split(beta,G,axis=1)
    beta_=np.stack( beta_, axis=0 )

    #print(gamma_.shape,"gamma_")

    """  
    x_=np.transpose(x_,axes=(0,1,3,4,2))
    x_=x_.reshape((-1,C))
    print(x_.shape,"last feed")

    out_,cache=layernorm_forward(x_,gamma_,beta_,gn_param)

    out_=out_.reshape((N,H,W,-1))
    out_=np.transpose(out_,axes=(0,3,1,2))

    print(out_.shape,"out_ shape")
    """
    ratio=(int)(C/G)
    #print(ratio,"ratio")
    cache={}


    for g in range (G):
      gammaG=gamma_[g,:,:,:,:].reshape(-1,1)
      betaG=beta_[g,:,:,:,:].reshape(-1,1)

      A=np.transpose(x_[g,:,:,:,:],axes=(0,2,3,1))
      A=A.reshape((-1,ratio))
      out_,cache[str(g)]=layernorm_forward(A,gammaG,betaG,gn_param)
      out_=np.reshape(out_,(N,H,W,ratio))
      out_=np.transpose(out_,axes=(0,3,1,2))
      
      
      #print(out_.shape,"out_")
      #print(A.shape,"A")
      out[:,g*ratio:(g+1)*ratio,:,:]=out_



    pass

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return out, cache


def spatial_groupnorm_backward(dout, cache):
    """
    Computes the backward pass for spatial group normalization.

    Inputs:
    - dout: Upstream derivatives, of shape (N, C, H, W)
    - cache: Values from the forward pass

    Returns a tuple of:
    - dx: Gradient with respect to inputs, of shape (N, C, H, W)
    - dgamma: Gradient with respect to scale parameter, of shape (C,)
    - dbeta: Gradient with respect to shift parameter, of shape (C,)
    """
    dx, dgamma, dbeta = None, None, None

    ###########################################################################
    # TODO: Implement the backward pass for spatial group normalization.      #
    # This will be extremely similar to the layer norm implementation.        #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    N, C, H, W=dout.shape
    G=len(cache)

    dx=np.zeros_like(dout)
    dgamma=np.zeros((C,))
    dbeta=np.zeros_like(dgamma)
    ratio=(int) (C/len(cache))

    dout_=np.split(dout,G,axis=1)
    dout_=np.stack(dout_,axis=0)
  

    for g in range (G):
      doutG=dout_[g,:,:,:,:]
      doutG=np.transpose(doutG,axes=(0,2,3,1))
      doutG=doutG.reshape((-1,ratio))
  

      temp,dgamma[g*ratio:(g+1)*ratio],dbeta[g*ratio:(g+1)*ratio] = layernorm_backward(doutG,cache[str(g)])

      """
      a,b,c=layernorm_backward(dout_[g,:,:,:,:],cache[str(g)])
      print(a.shape,"a")
      print(b.shape,"b")
      print(c.shape,"c")
      """
      temp=temp.reshape((N,H,W,ratio))
      temp=np.transpose(temp,axes=(0,3,1,2))
      dx[:,g*ratio:(g+1)*ratio,:,:]=temp
      
    pass

    #print(dgamma.shape,"my dgamma")
    dgamma=dgamma.reshape((1,dgamma.shape[0],1,1))
    dbeta=dbeta.reshape((1,dbeta.shape[0],1,1))

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return dx, dgamma, dbeta


def svm_loss(x, y):
    """
    Computes the loss and gradient using for multiclass SVM classification.

    Inputs:
    - x: Input data, of shape (N, C) where x[i, j] is the score for the jth
      class for the ith input.
    - y: Vector of labels, of shape (N,) where y[i] is the label for x[i] and
      0 <= y[i] < C

    Returns a tuple of:
    - loss: Scalar giving the loss
    - dx: Gradient of the loss with respect to x
    """
    N = x.shape[0]
    correct_class_scores = x[np.arange(N), y]
    margins = np.maximum(0, x - correct_class_scores[:, np.newaxis] + 1.0)
    margins[np.arange(N), y] = 0
    loss = np.sum(margins) / N
    num_pos = np.sum(margins > 0, axis=1)
    dx = np.zeros_like(x)
    dx[margins > 0] = 1
    dx[np.arange(N), y] -= num_pos
    dx /= N
    return loss, dx


def softmax_loss(x, y):
    """
    Computes the loss and gradient for softmax classification.

    Inputs:
    - x: Input data, of shape (N, C) where x[i, j] is the score for the jth
      class for the ith input.
    - y: Vector of labels, of shape (N,) where y[i] is the label for x[i] and
      0 <= y[i] < C

    Returns a tuple of:
    - loss: Scalar giving the loss
    - dx: Gradient of the loss with respect to x
    """
    shifted_logits = x - np.max(x, axis=1, keepdims=True)
    Z = np.sum(np.exp(shifted_logits), axis=1, keepdims=True)
    log_probs = shifted_logits - np.log(Z)
    probs = np.exp(log_probs)
    N = x.shape[0]
    loss = -np.sum(log_probs[np.arange(N), y]) / N
    dx = probs.copy()
    dx[np.arange(N), y] -= 1
    dx /= N
    return loss, dx
