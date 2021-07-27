%Definition of constants 

J = 4;           %Number of particles in each side 
w = 0.5;        %Width of problem 
b = 0.2;        %Distance between the two trains of particles 
dx = (w-b)/(2*J);%Distance between particles 
h = 1.1*dx;     %Smoothing length 
dt = 0.001;     %Time step 
F = 50;         %Tension in problem trains 
Totalsteps = 1500; %Total number of time steps 
%Definition of coordinates, Particle mass, Particle density, Particle 
%volume, Elasticity vector and speed vector

Xcoor_pil = [-w/2:dx:-w/2+J*dx]; Xcoor_pir = [b/2:dx:w/2]; 

for i=1:1:length(Xcoor_pil)-1     
    Xcoor_pal(i,1)=abs(Xcoor_pil(1,i+1)-Xcoor_pil(1,i))/2+Xcoor_pil(1,i);     
    Xcoor_par(i,1)=abs(Xcoor_pir(1,i+1)-Xcoor_pir(1,i))/2+Xcoor_pir(1,i);     
    particlemass_l(i,1)=abs(Xcoor_pil(1,i+1)-Xcoor_pil(1,i));     
    particlemass_r(i,1)=abs(Xcoor_pir(1,i+1)-Xcoor_pir(1,i)); 
end

Xcoor_particle=[Xcoor_pal; Xcoor_par];        %Particle coordinates
particlemass =[particlemass_l; particlemass_r]; %Particle mass
particledensity(1:2*J,1)=1;                    %Particle density
particlevolume=particlemass./particledensity;%Particle volume
E(1:2*J,1)=F;                                   %Particle elasticity
C=E/particledensity;                            %Particle Wavespeed

%Iinitial Displacement (Uini) and speed (Vini) 
Uini(1:J,1)=0; Uini(J+1:2*J,1)=0; Vini(1:J,1)=0.1; Vini(J+1:2*J,1)=-0.1; 

%Loop to solve the equation
Xcoor_particle0 = Xcoor_particle; 

for step = 1:Totalsteps     
    %Defining a matrix with values of d/dr*W used to find the derivate
    for i=1:length(Xcoor_particle)
        for j=1:length(Xcoor_particle)             
            Xdif = Xcoor_particle(j,1)-Xcoor_particle(i,1);             
            dKernelvalue(i,j) = -1.1284*Xdif/h^3*exp(-Xdif^2/h^2); 
        end
    end
    
    dFunction = zeros(2*J,1); ddFunction = zeros(2*J,1);    
    
    %First round of SPH diff. 1stderivative (2.14)                              
    
    for j=1:length(Xcoor_particle)        
        dFunction(j,1)=1/particledensity(j,1)*sum(dKernelvalue(:,j).*(particlemass.*(Uini-Uini(j,1)))); 
    end
    
    %Second round of SPH diff. 2nd derivative (2.15) 
    
    for j=1:length(Xcoor_particle)        
        ddFunction(j,1)=1/particledensity(j,1)*sum(dKernelvalue(:,j).*(particlemass.*(dFunction-dFunction(j,1))))*C(j,1); 
    end
    
    %Numericalintegration – Simple Euler & Update of coordinates (2.16)     
    Vini = Vini+ddFunction.*dt;    
    Uini = Uini+Vini.*dt;    
    Xcoor_particle = Xcoor_particle0+Uini;
end