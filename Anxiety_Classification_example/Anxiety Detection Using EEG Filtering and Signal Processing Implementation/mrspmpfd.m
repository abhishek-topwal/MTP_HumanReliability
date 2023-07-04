function [fd,fn,z,h,f,s,i1] = mrsp2mpfd(s,fs,np,nfft)
%
% Type: [fd,fn,z,h,f,s,i1] = mrsp2mpfd(s,fs,np,nfft);
%
% Inputs:
%
% s    := nt x nm matrix of modal responses
% fs   := 1 x 1 sample rate [Hz]
% np   := 1 x 1 # of points to use around peak for modal parameter fitting - default = 7
% nfft := 1 x 1 # of samples to use in fft - default = nt
%
%
% Outputs:
%
% fd   := nm x 1 damped frequencies [Hz]
% fn   := nm x 1 natural frequencies [Hz]
% z    := nm x 1 damping ratios [% critical]
% h    := nfft x nm fourier coef.
% f    := nfft x 1 frequency vector
% s    := nt x nm matrix of modal responses sorted by increasing frequency
% i1   := nm x 1 sorting index (used to sort by increasing frequency)
%
% Note: outputs are sorted by increasing damped frequency
%
%
% Compute modal parameters (freq., damp.) of free decay modal responses using
% frequency domain method.
%
% This function calls sdof_local
% See also: half_power mrsp2acorr sdof_id2
%
error(nargchk(2,4,nargin));
[rs,cs]=size(s);
if nargin < 3 | isempty(np)
 np=7;
end
if nargin < 4 | isempty(nfft)
 nfft=rs;
end
%
fd=zeros(cs,1);fn=fd;z=fd;h=zeros(nfft,cs);
f=[0:nfft-1].'*fs/(nfft);
for k=1:cs;
 h(:,k)=fft(s(:,k),nfft)/rs;
 [lam,r,fd1,z1] = sdof_local(h(:,k),f,np);
 fd(k,1)=fd1;
 z(k,1)=z1;
 fn(k,1)=fd1/sqrt(1+(z1/100)^2);
end
%
% sort by freq
%
[jnk,i1]=sort(fd);
fd=fd(i1);
fn=fn(i1);
z=z(i1);
s=s(:,i1);
h=h(:,i1);
%%