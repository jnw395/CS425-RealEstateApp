-- Mock data for neighborhood
INSERT INTO neighborhood VALUES 
('Downtown LA', 5.30, 'LA High', 'Central Park'),
('Brooklyn', 4.75, 'Brooklyn Tech', 'Prospect Park'),
('Lincoln Park', 3.50, 'Lincoln High', 'Lincoln Park'),
('Midtown Manhattan', 2.80, 'Stuyvesant', 'Bryant Park'),
('SoMa', 3.20, 'SOMA Academy', 'Yerba Buena Gardens');

-- Mock data for users
INSERT INTO "user" VALUES
('alice@example.com', 'Alice', 'Wong'),
('bob@example.com', 'Bob', 'Smith'),
('carla@example.com', 'Carla', 'Jones'),
('daniel@example.com', 'Daniel', 'Lee'),
('eva@example.com', 'Eva', 'Martinez');

-- Mock data for user_auth
INSERT INTO user_auth VALUES
('alice@example.com', 'hashedpw1', 'renter'),
('bob@example.com', 'hashedpw2', 'renter'),
('carla@example.com', 'hashedpw3', 'agent'),
('daniel@example.com', 'hashedpw4', 'agent'),
('eva@example.com', 'hashedpw5', 'renter');

-- Mock data for prospective_renter
INSERT INTO prospective_renter VALUES
('alice@example.com', '2025-07-01', 2500.00),
('bob@example.com', '2025-08-15', 1800.00),
('eva@example.com', '2025-06-10', 2200.00);

-- Mock data for agent
INSERT INTO agent VALUES
('carla@example.com', 'Senior Agent', 'DreamHomes LLC'),
('daniel@example.com', 'Broker', 'CityLife Realty');

-- Mock data for property
INSERT INTO property VALUES
('P0000001', 'Los Angeles', 'CA', 'Modern loft downtown', 2400.00, 850, 'carla@example.com', 'Downtown LA'),
('P0000002', 'Brooklyn', 'NY', 'Spacious 2-bedroom apartment', 2100.00, 950, 'daniel@example.com', 'Brooklyn'),
('P0000003', 'Chicago', 'IL', 'Cozy home near the park', 1800.00, 1000, 'carla@example.com', 'Lincoln Park'),
('P0000004', 'New York', 'NY', 'Luxury studio in Midtown', 3000.00, 600, 'daniel@example.com', 'Midtown Manhattan'),
('P0000005', 'San Francisco', 'CA', 'Stylish condo in SoMa', 2700.00, 700, 'carla@example.com', 'SoMa');

-- Mock data for house
INSERT INTO house VALUES
('P0000003', 3, 2);

-- Mock data for com_bldgs
INSERT INTO com_bldgs VALUES
('P0000004', 'Retail Store');

-- Mock data for apartments
INSERT INTO apartments VALUES
('P0000001', 1, 1, 'Loft'),
('P0000002', 2, 1, 'Walk-up'),
('P0000005', 2, 2, 'Condo');

-- Mock data for land
INSERT INTO land VALUES
('P0000006', 'Sandy', 'Flat', 'Residential');

-- Mock data for vacation_home
INSERT INTO vacation_home VALUES
('P0000007', 4, 3);

-- Mock data for amenities
INSERT INTO amenities VALUES
('P0000001', TRUE, TRUE, FALSE, TRUE),
('P0000002', TRUE, TRUE, TRUE, TRUE),
('P0000003', TRUE, FALSE, FALSE, TRUE),
('P0000004', FALSE, TRUE, TRUE, FALSE),
('P0000005', TRUE, TRUE, FALSE, TRUE);

-- Mock data for address
INSERT INTO address VALUES
('alice@example.com', '123', 'Main St', 'Los Angeles', 'CA', '90012'),
('bob@example.com', '456', 'Maple Ave', 'Brooklyn', 'NY', '11201'),
('eva@example.com', '789', 'Lakeview Rd', 'Chicago', 'IL', '60614');

-- Mock data for credit_card
INSERT INTO credit_card VALUES
('alice@example.com', '1111222233334444', '2026-10-01', '123'),
('bob@example.com', '5555666677778888', '2025-07-01', '456'),
('eva@example.com', '9999000011112222', '2027-03-01', '789');

-- Mock data for preferred_loc
INSERT INTO preferred_loc VALUES
('alice@example.com', 'San Francisco', 'CA', 1),
('bob@example.com', 'New York', 'NY', 1),
('eva@example.com', 'Chicago', 'IL', 2);

-- Mock data for booking
INSERT INTO booking VALUES
('B0000001', '2025-05-01', 100, '1111222233334444', '2025-07-01', '2025-07-31', 'alice@example.com', 'P0000002'),
('B0000002', '2025-05-03', 80, '5555666677778888', '2025-08-01', '2025-08-30', 'bob@example.com', 'P0000001');

-- Mock data for makes
INSERT INTO makes VALUES
('alice@example.com', 'B0000001'),
('bob@example.com', 'B0000002');

-- Mock data for looks_at
INSERT INTO looks_at VALUES
('carla@example.com', 'B0000001'),
('daniel@example.com', 'B0000002');

-- Mock data for reward_program
INSERT INTO reward_program VALUES
('RWD001', 100, TRUE, 'alice@example.com'),
('RWD002', 80, FALSE, 'bob@example.com'),
('RWD003', 120, TRUE, 'eva@example.com');

