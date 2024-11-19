const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 5000;

app.use(bodyParser.json());
app.use(cors());

mongoose.connect('mongodb://localhost/internship_management', { useNewUrlParser: true, useUnifiedTopology: true });

const db = mongoose.connection;
db.on('error', console.error.bind(console, 'connection error:'));
db.once('open', () => {
  console.log('Connected to MongoDB');
});

// Routes
const registerRoutes = require('./routes/register');
const mentorRoutes = require('./routes/mentor');
const coordinatorRoutes = require('./routes/coordinator');
const contactRoutes = require('./routes/contact');

app.use('/api/register', registerRoutes);
app.use('/api/mentor', mentorRoutes);
app.use('/api/coordinator', coordinatorRoutes);
app.use('/api/contact', contactRoutes);

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});

const mongoose = require('mongoose');

const internshipSchema = new mongoose.Schema({
  startDate: Date,
  companyName: String,
  companyAddress: String,
  externalMentorName: String,
  externalMentorContact: String,
  externalMentorEmail: String,
  companyRegNumber: String,
  city: String,
  stipend: Number,
  offerLetter: String,
});

module.exports = mongoose.model('Internship', internshipSchema);

const mongoose = require('mongoose');

const reportSchema = new mongoose.Schema({
  internId: mongoose.Schema.Types.ObjectId,
  report: String,
  assignment: String,
  evaluation: String,
});

module.exports = mongoose.model('Report', reportSchema);
const express = require('express');
const router = express.Router();
const Internship = require('../models/Internship');

router.post('/', async (req, res) => {
  try {
    const internship = new Internship(req.body);
    await internship.save();
    res.status(201).send(internship);
  } catch (error) {
    res.status(400).send(error);
  }
});

module.exports = router;
const express = require('express');
const router = express.Router();
const Internship = require('../models/Internship');

router.get('/', async (req, res) => {
  try {
    const internships = await Internship.find();
    res.status(200).send(internships);
  } catch (error) {
    res.status(400).send(error);
  }
});

module.exports = router;
const express = require('express');
const router = express.Router();

router.post('/', (req, res) => {
  // Handle contact form submission
  res.status(200).send('Contact form submitted');
});

module.exports = router;
