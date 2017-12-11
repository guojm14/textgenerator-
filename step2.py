import tensorflow as tf
import numpy as np
from PIL import Image
from trans import TPS_STN
import os


nx=5
ny=2
#t_img = tf.constant(img.reshape(shape), dtype=tf.float32)
s_img=tf.placeholder(tf.float32,[1,64,256,3])
p_=tf.placeholder(tf.float32,[nx*ny,3])
W_inv_t=tf.placeholder(tf.float32,[nx*ny+3,nx*ny+3])
t_img = TPS_STN(s_img, nx, ny,p_,W_inv_t,[64,256,3])
def getpw():
    if 1:
        gx = 2. / (nx-1) # grid x size
        gy = 2. / (ny-1) # grid y size
        cx = -1.  # x coordinate
        cy = -1.  # y coordinate


        p_ = np.empty([nx*ny, 3], dtype='float32')
        i = 0
        for _ in range(ny):
          for _ in range(nx):
            p_[i, :] = 1, cx, cy
            i += 1
            cx += gx
          cx = -1.
          cy += gy
        p_=p_/3
        offsetx=np.random.random(2)+2
        offsety=2*np.random.random(nx*ny)+1
        
        for i in range(ny):
          for j in range(nx):
            p_[i*nx+j, 2] =p_[i*nx+j, 2]*offsety[i*nx+j]
            p_[i*nx+j, 1] =p_[i*nx+j, 1]*offsetx[i]
            p_[i*nx+j,0]=1

        p_1 = p_.reshape([nx*ny,1,3])
        p_2 = p_.reshape([1, nx*ny, 3])
        d = np.sqrt(np.sum((p_1-p_2)**2, 2)) # [nx*ny, nx*ny]
        r = d*d*np.log(d*d+1e-5)
        W = np.zeros([nx*ny+3, nx*ny+3], dtype='float32')
        W[:nx*ny, 3:] = r
        W[:nx*ny, :3] = p_
        W[nx*ny:, 3:] = p_.T
        W_inv = np.linalg.inv(W)
    return p_,W_inv


fop=open('list.txt','w')
with tf.Session() as sess:
  sess.run(tf.initialize_all_variables())
  for item in os.listdir('result'):
      if 1:
          print item
          p,W_inv=getpw()
          img=np.array(Image.open('result/'+item).resize([256,64])).reshape([1,64,256,3])
      
          img1 = sess.run(t_img,feed_dict={s_img:img,p_:p,W_inv_t:W_inv})
          Image.fromarray(np.uint8(img1.reshape([64,256,3]))).save('transresult/'+item)
          fop.write(item+' ')
          for i in xrange(nx*ny):
              for j in xrange(2):
                  fop.write(str(p[i,j+1])+' ')
          fop.write('\n')
      #except:
      #   print 'error'
      
          
          
