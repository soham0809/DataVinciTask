CREATE TABLE IF NOT EXISTS campaigns (
  id INTEGER PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  status VARCHAR(20) NOT NULL,
  clicks INTEGER NOT NULL,
  cost NUMERIC(10, 2) NOT NULL,
  impressions INTEGER NOT NULL
);

INSERT INTO campaigns (id, name, status, clicks, cost, impressions) VALUES
  (1, 'Summer Sale', 'Active', 150, 45.99, 1000),
  (2, 'Black Friday', 'Paused', 320, 89.50, 2500),
  (3, 'New Year Blast', 'Active', 210, 60.00, 1800),
  (4, 'Spring Clearance', 'Paused', 90, 25.75, 900),
  (5, 'Back to School', 'Active', 300, 99.99, 2700),
  (6, 'Holiday Specials', 'Active', 180, 55.25, 1500),
  (7, 'Clearance Bonanza', 'Paused', 75, 19.99, 800),
  (8, 'Weekend Flash Sale', 'Active', 260, 70.10, 2200),
  (9, 'Referral Program', 'Active', 140, 40.00, 1200),
  (10, 'Loyalty Rewards', 'Paused', 110, 35.50, 950);



