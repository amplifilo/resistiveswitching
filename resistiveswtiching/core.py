from .modules import *


class TimeTrace:
    def __init__(self, trace, time=None):
        self.trace = trace
        self.time = time

    def get_fft_values(self, T, N, f_s):
        N2 = 2 ** (int(np.log2(N)) + 1) # round up to next highest power of 2
        f_values = np.linspace(0.0, 1.0/(2.0*T), N2//2)
        fft_values_ = fft(self.trace)
        fft_values = 2.0/N2 * np.abs(fft_values_[0:N2//2])
        return f_values, fft_values

    def plot_wavelet(self, scales, 
                    waveletname = 'cmor',
                    **kwargs): 
                    
        if self.time is None:
            time = kwargs["time"]
        else:
            time = self.time

        dt = time[1] - time[0]
        [coefficients, frequencies] = pywt.cwt(self.trace, scales, waveletname, dt)
        power = (abs(coefficients)) ** 2
        period = 1. / frequencies
        levels = [0.0625, 0.125, 0.25, 0.5, 1, 2, 4, 8]
        contourlevels = np.log2(levels)
        
        fig, ax = plt.subplots(figsize=(15, 10))
        im = ax.contourf(time, np.log2(period), np.log2(power), contourlevels, extend='both')
        
        ax.set_title(title, fontsize=20)
        ax.set_ylabel(ylabel, fontsize=18)
        ax.set_xlabel(xlabel, fontsize=18)
        
        yticks = 2**np.arange(np.ceil(np.log2(period.min())), np.ceil(np.log2(period.max())))
        ax.set_yticks(np.log2(yticks))
        ax.set_yticklabels(yticks)
        ax.invert_yaxis()
        ylim = ax.get_ylim()
        ax.set_ylim(ylim[0], -1)
        
        cbar_ax = fig.add_axes([0.95, 0.5, 0.03, 0.25])
        fig.colorbar(im, cax=cbar_ax, orientation="vertical")
        

    def get_ave_values(self, xvalues, yvalues, n = 5):
        
        signal_length = len(self.time)
        if signal_length % n == 0:
            padding_length = 0
        else:
            padding_length = n - signal_length//n % n
        xarr = np.array(self.time)
        yarr = np.array(self.trace)
        xarr.resize(signal_length//n, n)
        yarr.resize(signal_length//n, n)
        xarr_reshaped = xarr.reshape((-1,n))
        yarr_reshaped = yarr.reshape((-1,n))
        x_ave = xarr_reshaped[:,0]
        y_ave = np.nanmean(yarr_reshaped, axis=1)
        return x_ave, y_ave


    
    def plot_signal_plus_average(self, average_over = 5):
        fig, ax = plt.subplots(figsize=(15, 3))
        time_ave, signal_ave = get_ave_values(self.time, self.signal, average_over)
        ax.plot(time, signal, label='signal')
        ax.plot(time_ave, signal_ave, label = 'time average (n={})'.format(5))
        ax.set_xlim([time[0], time[-1]])
        ax.set_ylabel('Signal Amplitude', fontsize=18)
        ax.set_title('Signal + Time Average', fontsize=18)
        ax.set_xlabel('Time', fontsize=18)
        ax.legend()
        
    
    def get_fft_values(self, T, N, f_s):
        f_values = np.linspace(0.0, 1.0/(2.0*T), N//2)
        fft_values_ = fft(self.trace)
        fft_values = 2.0/N * np.abs(fft_values_[0:N//2])
        return f_values, fft_values
    
    def plot_fft_plus_power(self):
        dt = self.time[1] - self.time[0]
        N = len(self.trace)
        fs = 1/dt
        
        fig, ax = plt.subplots(figsize=(15, 3))
        variance = np.std(self.trace)**2
        f_values, fft_values = self.get_fft_values(self.signal, dt, N, fs)
        fft_power = variance * abs(fft_values) ** 2     # FFT power spectrum
        ax.plot(f_values, fft_values, 'r-', label='Fourier Transform')
        ax.plot(f_values, fft_power, 'k--', linewidth=1, label='FFT Power Spectrum')
        ax.set_xlabel('Frequency [Hz / year]', fontsize=18)
        ax.set_ylabel('Amplitude', fontsize=18)
        ax.legend()
