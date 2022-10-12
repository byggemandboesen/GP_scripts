clear;
clc;

% Prism
%% variables to change
x_min = -20e3;  
x_max = 20e3;

% Anomalous density block 1
size1 = [2e3,2e3,2e3]; % (dx,dy,dz)
depth1 = 4e3; % the depth were the anomaly starts
drho1= 400; % the difference in density
center1 =  -10000; % The location of the maximum

% Anomalous density block 2
size2 = [2e3,2e3,2e3]; % (dx,dy,dz)
depth2 = 0.05e3; % the depth were the anomaly starts
drho2= 400; % the difference in density
center2 =  2500; % The location of the maximum


% Anomalous density block 3
size3 = [2e3,2e3,2e3]; % (dx,dy,dz)
depth3 = 5e3; % the depth were the anomaly starts
drho3= 400; % the difference in density
center3 =  6000; % The location of the maximum
%%

% Use function, gravprism(), from Donald L. Turcotte & Gerald Schubert: Geodynamics.
x = linspace(x_max,x_min); % Generates 200 values of x between max and min.
dg1=gravprism(drho1,x-size1(1)/2-center1,x+size1(1)/2-center1,-size1(2)/2,size1(2)/2,depth1,depth1+size1(3));
dg2=gravprism(drho2,x-size2(1)/2-center2,x+size2(1)/2-center2,-size2(2)/2,size2(2)/2,depth2,depth2+size2(3));
dg3=gravprism(drho3,x-size3(1)/2-center3,x+size3(1)/2-center3,-size3(2)/2,size3(2)/2,depth3,depth3+size3(3));

figure()
plot(x,dg1+dg2+dg3)

% plot 
figure()
plot(x,dg1)
hold
plot(x,dg2)
plot(x,dg3)
plot(x,dg1+dg2+dg3)
xlabel('x(m)')
ylabel('gravity anomaly(mgal)')
legend('Anomaly 1','Anomaly 2','Anomaly 3','sum')