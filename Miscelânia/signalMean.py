# we use numpy to compute the mean of an array of values
import numpy

 # let's define a new box class that inherits from OVBox
 class MyOVBox(OVBox):
    def __init__(self):
    OVBox.__init__(self)
    # we add a new member to save the signal header information we will receive
    self.signalHeader = None

    # The process method will be called by openvibe on every clock tick
    def process(self):
       # we iterate over all the input chunks in the input buffer
       for chunkIndex in range( len(self.input[0]) ):
          # if it's a header we save it and send the output header (same as input, except it has only one channel named 'Mean'
          if(type(self.input[0][chunkIndex]) == OVSignalHeader):
             self.signalHeader = self.input[0].pop()
             outputHeader = OVSignalHeader(
             self.signalHeader.startTime,
             self.signalHeader.endTime,
             [1, self.signalHeader.dimensionSizes[1]],
             ['Mean']+self.signalHeader.dimensionSizes[1]*[''],
             self.signalHeader.samplingRate)
             self.output[0].append(outputHeader)

          # if it's a buffer we pop it and put it in a numpy array at the right dimensions
          # We compute the mean and add the buffer in the box output buffer
          elif(type(self.input[0][chunkIndex]) == OVSignalBuffer):
             chunk = self.input[0].pop()
             numpyBuffer = numpy.array(chunk).reshape(tuple(self.signalHeader.dimensionSizes))
             numpyBuffer = numpyBuffer.mean(axis=0)
             chunk = OVSignalBuffer(chunk.startTime, chunk.endTime, numpyBuffer.tolist())
             self.output[0].append(chunk)
          # if it's a end-of-stream we just forward that information to the output
          elif(type(self.input[0][chunkIndex]) == OVSignalEnd):
             self.output[0].append(self.input[0].pop())

 # Finally, we notify openvibe that the box instance 'box' is now an instance of MyOVBox.
 # Don't forget that step !!
 box = MyOVBox()
