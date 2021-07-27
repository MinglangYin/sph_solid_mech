clear all
close all
clc


N=50;    %Number of particles (boundary particles excluded) 
L=2;     %Length of string
c=1;     %Wave speed c^2 = F/rho 
dx=L/N;%Distance bewteen particles
bo=2;    %Number of boundary particles on each side of problem domain
n=2*bo+N;%Total number of particles 
h=1.1*dx;%Smoothing length for all particles 
dt=0.001; %Size of timestep
Totalsteps=50;

%Definition of coordinates, Particle volume, initial values u(x) 
%and d/dx*u(x)=v

Xcord_point = linspace(0, 1, N)';
ParticleVol(1:N,1) = dx;

u_ini = 0.5*Xcord_point; 
v_ini = zeros(N,1); 

%Defining a matrix with values of d/dx*W used to find the derivate in each 
%timestep

for i=1:N
    for j=1:N        
        Xdif = Xcord_point(j,1)-Xcord_point(i,1);         
        dKernelvalue(i,j) = -1.1284*Xdif/h^3*exp(-Xdif^2/h^2); %(2.10)
    end
end

%Loop to solve Equation (2.1)
for step=1:Totalsteps     
    dFunction = zeros(N,1);    
    ddFunction = zeros(N,1);
    
    %First round of SPH diff. 1st derivate (2.4)        
    for j=1:N        
        dFunction(j,1) = sum(dKernelvalue(:,j).*ParticleVol.*u_ini); 
    end
   
    
    %Numerical integration – Simple Euler & Update of    
    %initial values (2.11)     
    v_new = v_ini + dFunction.*dt;     
    u_ini = u_ini + v_new.*dt;     
    v_ini = v_new;
    
    v_ini(1) =0;
    u_ini(1) =0 ;
    
    plot(u_ini)
    plot(v_ini)
    
end