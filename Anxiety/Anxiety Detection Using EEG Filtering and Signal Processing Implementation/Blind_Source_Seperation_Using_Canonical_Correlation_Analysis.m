% ------------------------------YGBSS.m--------------------------------
function [source,A]=YGBSS(X, L, e1,e2,e3,n)
%  input
%  X   is the recorded signals.
%  L   is the length of window function.
%  e1  is the threshold value for peak detection. Lower value may lead to more sources being separated.
%  e2  is the value of consine distance.
%  e3  is the threshold alue for removing low energy points. Because the low energy points always contain noise.
%  n   is the number of channel to filter all sources.
%  output
%  source is the separated sources
%  A is the absolute value of mixing matrix.
[m, T] = size(X);
if m>T
 error('X must be row vectors');
end
if m<2
 error('X must have two row at least');
end
if nargin < 2,
L = floor(T/4); 
L=L+1-rem(L,2); 
end
if nargin < 3,e1 = 0.1;    end   %threshold value for peak detection
if nargin < 4,e2 = 0.004;  end   %consine distance
if nargin < 5,e3 = 0.1;    end   %threshold value for removing low energy points
if nargin < 6,n  = 1;      end   %the number of channel to filter all sources
if n>m
 error('n must be less than row vectors');
end
h=hamming(L); 
for i=1:m
coefs(i,:,:)=tfrstft(X(i,:)',1:T,T,h,1);
end
for i=1:m
energy(i,:)=sum(abs(squeeze(coefs(i,:,:))').^2);
end
%scatter plot of energy function
%figure
%plot(energy(1,:),energy(2,:),'.');hold on
%plot3(energy(1,:),energy(2,:),energy(3,:),'.');hold on
energysum=sum(energy);
delta = max(abs(energysum))*e1; 
[maxtab, mintab]=peakdet(energysum, delta);
[m1 n1]=size(maxtab);
%sum of energy function
%figure
%plot(energysum);hold on;
%for i=1:m1
%plot((maxtab(i,1)),maxtab(i,2),'*','color','r');
%end
% 2D scatter
%figure
%plot(energy(1,:),energy(2,:),'.');hold on
%plot(energy(1,maxtab(:,1)),energy(2,maxtab(:,1)),'*','color','r');hold on
masks=zeros(m1/2,T);
for i=1:T
for j=1:m1/2
if sum(energy(:,i))>e3*sum(energy(:,maxtab(j,1)))
if pdist([energy(1:end,i)';energy(1:end,maxtab(j,1))'],'cosine')<e2
masks(j,i)=1;
end
end
end
end
for j=1:m1/2
maskss=zeros(T,T);
for i=1:T
maskss(:,i)=masks(j,:)';
end
source(j,:)=tfristft(squeeze(coefs(n,:,:)).*maskss,1:T,h,1);
end
[hrow,hcol]=size(h); Lh=(hrow-1)/2;
h=h/norm(h);
for i=1:T
tau=-min([round(T/2)-1,Lh,i-1]):min([round(T/2)-1,Lh,T-i]);
pad(i)=(sum(h)/(sum(h(Lh+1+tau)))).^(1/1.6);
end
%padding line
%figure
%plot(pad);
%xlabel('Padding line');
for j=1:m1/2
source(j,:)=source(j,:).*pad;
end
A=(energy(:,maxtab(1:m1/2,1))).^(0.5);
A=A./repmat(sqrt(sum(A.^2,1)),size(A,1),1);