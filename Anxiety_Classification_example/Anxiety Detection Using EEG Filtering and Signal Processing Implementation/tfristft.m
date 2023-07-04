function [x,t] = tfristft(tfr,t,h,trace);
%TFRISTFT Inverse Short time Fourier transform.
%	[X,T]=TFRSTFT(tfr,T,H,TRACE) computes the inverse short-time 
%	Fourier transform of a discrete-time signal X. This function
%	may be used for time-frequency synthesis of signals.
% 
%	X     : signal.
%	T     : time instant(s)          (default : 1:length(X)).
%	H     : frequency smoothing window, H being normalized so as to
%	        be  of unit energy.      (default : Hamming(N/4)). 
%	TRACE : if nonzero, the progression of the algorithm is shown
%	                                 (default : 0).
%	TFR   : time-frequency decomposition (complex values). The
%	        frequency axis is graduated from -0.5 to 0.5.
%
%	Example :
%        t=200+(-128:127); sig=[fmconst(200,0.2);fmconst(200,0.4)]; 
%        h=hamming(57); tfr=tfrstft(sig,t,256,h,1);
%        sigsyn=tfristft(tfr,t,h,1);
%        plot(t,abs(sigsyn-sig(t)))
% 
if (nargin<3),
 error('At least 3 parameters required');
elseif (nargin==3),
 trace=0;
end;
[N,NbPoints]=size(tfr);
[trow,tcol] =size(t);
[hrow,hcol] =size(h); Lh=(hrow-1)/2; 
if (trow~=1),
 error('T must only have one row'); 
elseif (hcol~=1)|(rem(hrow,2)==0),
 error('H must be a smoothing window with odd length');
elseif (tcol~=NbPoints)
 error('tfr should have as many columns as t has rows.');
end; 
Deltat=t(2:tcol)-t(1:tcol-1); 
Mini=min(Deltat); Maxi=max(Deltat);
if (Mini~=1) & (Maxi~=1),
 error('The tfr must be computed at each time sample.');
end;
h=h/norm(h);
tfr=ifft(tfr);
x=zeros(tcol,1);
for icol=1:tcol,
 valuestj=max([1,icol-N/2,icol-Lh]):min([tcol,icol+N/2,icol+Lh]);
 for tj=valuestj,
  tau=icol-tj; indices= rem(N+tau,N)+1; 
  % fprintf('%g %g %g\n',tj,tau,indices);
  x(icol,1)=x(icol,1)+tfr(indices,tj)*h(Lh+1+tau);
 end;
 x(icol,1)=x(icol,1)/sum(abs(h(Lh+1+icol-valuestj)).^2);
end;