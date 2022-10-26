function [RMS] = RootMeanSq(Degree,Order,Year)
% Input :
% Degree 
% Order 
% Year (5 year increments, 1900 to 2015)
% Output :
% RootMeanSquare value for the chosen degree, maximum order and year. 
if Order > Degree
   error('Error. Degree can not be higher than Order.')
end
opts = detectImportOptions('Gauss_Coefficients.txt');
opts.DataLines = 4;
data = readtable('Gauss_Coefficients.txt',opts);         %load data
years = data{1,4:end};                              %define years
Deg = data{2:end,2};                    %define degree
Ord = data{2:end,3};                    %define Order
Coeff = data{2:end,4:end};                          %define coefficient matrix
RMS = sqrt((Degree+1)*sum(Coeff(find(Deg(:) == Degree & Ord(:) <= Order),find(years == Year)).^2));
% search for index in rows corresponding to the chosen degree and maximum order,
% and search for the index in coloumns based on year chosen. Take these out
% from the coefficient matrix and calculate the RMS.
end