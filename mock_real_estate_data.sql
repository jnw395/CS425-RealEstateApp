-- Insert data into neighborhood
INSERT INTO neighborhood (neighborhood_name, crime_rate, nearby_schools, nearby_parks) VALUES
('Downtown', 8.5, 'Central High', 'Millennium Park'),
('Uptown', 6.2, 'Northwood Elem', 'Riverside Park'),
('Midtown', 7.8, 'City College', 'Central Park'),
('Suburbia', 3.1, 'Greenwood Schl', 'Community Park'),
('Hillside', 9.1, 'South HS', 'Overlook Park'),
('Lakeshore', 4.5, 'Lakeview Elem', 'Beachfront Park'),
('Westside', 6.8, 'West HS', 'Freedom Park'),
('Eastwood', 5.5, 'Eastwood MS', 'Valley Park'),
('Northgate', 4.9, 'Northgate HS', 'Terrace Park'),
('Southgate', 7.2, 'Southgate MS', 'Meadow Park');
INSERT INTO "user" (email, first_name, last_name) VALUES
('john.doe@example.com', 'John', 'Doe'),
('jane.smith@example.com', 'Jane', 'Smith'),
('robert.jones@example.com', 'Robert', 'Jones'),
('alice.brown@example.com', 'Alice', 'Brown'),
('michael.davis@example.com', 'Michael', 'Davis'),
('sarah.wilson@example.com', 'Sarah', 'Wilson'),
('david.garcia@example.com', 'David', 'Garcia'),
('linda.rodriguez@example.com', 'Linda', 'Rodriguez'),
('christopher.williams@example.com', 'Christopher', 'Williams'),
('angela.garner@example.com', 'Angela', 'Garner');
INSERT INTO prospective_renter (email, desired_move_in_date, budget) VALUES
('john.doe@example.com', '2024-09-01', 2500.00),
('jane.smith@example.com', '2024-10-15', 3000.00),
('robert.jones@example.com', '2024-11-01', 2000.00),
('alice.brown@example.com', '2024-12-01', 3500.00),
('michael.davis@example.com', '2025-01-15', 2800.00);
INSERT INTO agent (email, job_title, real_estate_agency) VALUES
('sarah.wilson@example.com', 'Senior Agent', 'Acme Realty'),
('david.garcia@example.com', 'Junior Agent', 'Global Homes'),
('linda.rodriguez@example.com', 'Broker', 'Prestige Properties'),
('christopher.williams@example.com', 'Agent', 'Citywide Realty'),
('angela.garner@example.com', 'Agent', 'Legacy Realty');
INSERT INTO property (property_id, city, p_state, description, price, sq_footage, availability, property_type, email, neighborhood_name) VALUES
('P1001', 'Chicago', 'IL', 'Luxury House with Lake View', 350000.00, 2500, TRUE, 'House', 'sarah.wilson@example.com', 'Lakeshore'),
('P1002', 'New York', 'NY', 'Cozy Apartment in Downtown', 200000.00, 1200, TRUE, 'Apartment', 'david.garcia@example.com', 'Downtown'),
('P1003', 'New York', 'NY', 'Commercial Building in Midtown', 500000.00, 4000, FALSE, 'Commercial', 'linda.rodriguez@example.com', 'Midtown'),
('P1004', 'Los Angeles', 'CA', 'Spacious Land in Suburbia', 150000.00, 10000, TRUE, 'Land', 'christopher.williams@example.com', 'Suburbia'),
('P1005', 'Miami', 'FL', 'Vacation Home near Beach', 400000.00, 2000, TRUE, 'Vacation Home', 'angela.garner@example.com', 'Lakeshore'),
('P1006', 'Chicago', 'IL', 'Modern House in Uptown', 420000.00, 2700, TRUE, 'House', 'sarah.wilson@example.com', 'Uptown'),
('P1007', 'Seattle', 'WA', 'Small Apartment in Westside', 180000.00, 950, TRUE, 'Apartment', 'david.garcia@example.com', 'Westside'),
('P1008', 'New York', 'NY', 'Large Commercial Building', 675000, 5500, FALSE, 'Commercial', 'linda.rodriguez@example.com', 'Midtown'),
('P1009', 'Los Angeles', 'CA', 'Land for Development', 225000, 12000, TRUE, 'Land', 'christopher.williams@example.com', 'Suburbia'),
('P1010', 'Miami', 'FL', 'Luxury Vacation Home', 550000, 2300, TRUE, 'Vacation Home', 'angela.garner@example.com', 'Lakeshore');
INSERT INTO house (property_id, num_bedrooms, num_bathrooms) VALUES
('P1001', 4, 3),
('P1006', 3, 2);
INSERT INTO com_bldgs (property_id, type_of_business) VALUES
('P1003', 'Office'),
('P1008', 'Retail');
INSERT INTO apartments (property_id, num_bedrooms, num_bathrooms, bldg_type) VALUES
('P1002', 2, 2, 'Studio'),
('P1007', 1, 1, 'Condo'),
('P1009', 2, 2, 'Condo');
INSERT INTO land (property_id, soil_type, topography, zoning) VALUES
('P1004', 'Clay', 'Flat', 'Residential'),
('P1009', 'Loam', 'Slope', 'Commercial');
INSERT INTO vacation_home (property_id, num_bedrooms, num_bathrooms) VALUES
('P1005', 3, 2),
('P1010', 4, 3);
INSERT INTO booking (booking_id, booking_date, reward_pts_earned, card_number, start_date, end_date, email, property_id) VALUES
('B2001', '2024-08-01', 100, '1234567890123456', '2024-09-01', '2024-09-07', 'john.doe@example.com', 'P1002'),
('B2002', '2024-09-01', 150, '9876543210987654', '2024-10-15', '2024-10-22', 'jane.smith@example.com', 'P1001'),
('B2003', '2024-10-01', 80, '4567890123456789', '2024-11-01', '2024-11-08', 'robert.jones@example.com', 'P1007'),
('B2004', '2024-11-01', 200, '5678901234567890', '2024-12-01', '2024-12-08', 'alice.brown@example.com', 'P1005'),
('B2005', '2024-12-01', 120, '6789012345678901', '2025-01-15', '2025-01-22', 'michael.davis@example.com', 'P1006');
INSERT INTO address (email, house_number, street, city, addr_state, zip_code) VALUES
('john.doe@example.com', '123', 'Main St', 'Chicago', 'IL', '60601'),
('jane.smith@example.com', '456', 'Oak Ave', 'New York', 'NY', '10001'),
('robert.jones@example.com', '789', 'Pine Ln', 'New York', 'NY', '10002'),
('alice.brown@example.com', '101', 'Elm St', 'Los Angeles', 'CA', '90001'),
('michael.davis@example.com', '222', 'Lakeview Dr', 'Los Angeles', 'CA', '90002'),
('john.doe@example.com', '125', 'Main St', 'Chicago', 'IL', '60601'),
('jane.smith@example.com', '458', 'Oak Ave', 'New York', 'NY', '10001'),
('robert.jones@example.com', '790', 'Pine Ln', 'New York', 'NY', '10002'),
('alice.brown@example.com', '103', 'Elm St', 'Los Angeles', 'CA', '90001'),
('michael.davis@example.com', '224', 'Lakeview Dr', 'Los Angeles', 'CA', '90002');
INSERT INTO credit_card (email, card_number, expiration_date, CVV, billing_house_number, billing_street, billing_city, billing_state, billing_zip) VALUES
('john.doe@example.com', '1234567890123456', '2025-12-31', '123', '123', 'Main St', 'Chicago', 'IL', '60601'),
('jane.smith@example.com', '9876543210987654', '2026-01-31', '456', '456', 'Oak Ave', 'New York', 'NY', '10001'),
('robert.jones@example.com', '4567890123456789', '2027-02-28', '789', '789', 'Pine Ln', 'New York', 'NY', '10002'),
('alice.brown@example.com', '5678901234567890', '2028-03-31', '012', '101', 'Elm St', 'Los Angeles', 'CA', '90001'),
('michael.davis@example.com', '6789012345678901', '2029-04-30', '345', '222', 'Lakeview Dr', 'Los Angeles', 'CA', '90002');
INSERT INTO preferred_loc (email, city, pre_state, priority) VALUES
('john.doe@example.com', 'Chicago', 'IL', 1),
('jane.smith@example.com', 'New York', 'NY', 1),
('robert.jones@example.com', 'New York', 'NY', 2),
('alice.brown@example.com', 'Los Angeles', 'CA', 1),
('michael.davis@example.com', 'Los Angeles', 'CA', 1);
INSERT INTO amenities (property_id, kitchen, wifi, pool, laundry) VALUES
('P1001', TRUE, TRUE, TRUE, TRUE),
('P1002', TRUE, TRUE, FALSE, TRUE),
('P1003', TRUE, FALSE, FALSE, FALSE),
('P1004', FALSE, FALSE, FALSE, FALSE),
('P1005', TRUE, TRUE, TRUE, FALSE),
('P1006', TRUE, TRUE, FALSE, TRUE),
('P1007', TRUE, TRUE, FALSE, TRUE),
('P1008', FALSE, FALSE, FALSE, FALSE),
('P1009', FALSE, FALSE, FALSE, FALSE),
('P1010', TRUE, TRUE, TRUE, TRUE);
INSERT INTO looks_at (email, booking_id) VALUES
('sarah.wilson@example.com', 'B2001'),
('david.garcia@example.com', 'B2002'),
('linda.rodriguez@example.com', 'B2003'),
('christopher.williams@example.com', 'B2004'),
('angela.garner@example.com', 'B2005');
INSERT INTO makes (email, booking_id) VALUES
('john.doe@example.com', 'B2001'),
('jane.smith@example.com', 'B2002'),
('robert.jones@example.com', 'B2003'),
('alice.brown@example.com', 'B2004'),
('michael.davis@example.com', 'B2005');
INSERT INTO reward_program (reward_id, reward_pts, enrolled, email) VALUES
('R3001', 100, TRUE, 'john.doe@example.com'),
('R3002', 150, TRUE, 'jane.smith@example.com'),
('R3003', 80, TRUE, 'robert.jones@example.com'),
('R3004', 200, TRUE, 'alice.brown@example.com'),
('R3005', 120, TRUE, 'michael.davis@example.com');
INSERT INTO user_auth (email, password, role) VALUES
('john.doe@example.com', 'password123', 'renter'),
('jane.smith@example.com', 'password456', 'renter'),
('robert.jones@example.com', 'password789', 'renter'),
('alice.brown@example.com', 'password101', 'renter'),
('michael.davis@example.com', 'password222', 'renter'),
('sarah.wilson@example.com', 'agentpass', 'agent'),
('david.garcia@example.com', 'agentpass2', 'agent'),
('linda.rodriguez@example.com', 'brokerpass', 'agent'),
('christopher.williams@example.com', 'agentpass3', 'agent'),
('angela.garner@example.com', 'agentpass4', 'agent');
