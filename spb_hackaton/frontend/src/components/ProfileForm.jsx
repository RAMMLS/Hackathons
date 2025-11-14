import { useState } from 'react';
import './ProfileForm.css';

export default function ProfileForm({ onSubmit, isLoading }) {
  const [formData, setFormData] = useState({
    name: '',
    age: '',
    profession: '',
    interests: '',
    education: '',
    location: '',
    bio: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Convert interests string to array
    const interestsArray = formData.interests
      .split(',')
      .map(item => item.trim())
      .filter(item => item.length > 0);

    // Validate required fields
    if (!formData.name || !formData.age || !formData.profession || interestsArray.length === 0) {
      alert('Please fill in all required fields: Name, Age, Profession, and at least one Interest');
      return;
    }

    const profileData = {
      ...formData,
      age: parseInt(formData.age),
      interests: interestsArray
    };

    onSubmit(profileData);
  };

  return (
    <div className="profile-form-container">
      <h2>Tell Us About Yourself</h2>
      <p className="form-description">
        Fill in your profile information and our AI will create a personalized article 
        with topics of interest just for you!
      </p>
      
      <form onSubmit={handleSubmit} className="profile-form">
        <div className="form-group">
          <label htmlFor="name">
            Name <span className="required">*</span>
          </label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
            placeholder="John Doe"
          />
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="age">
              Age <span className="required">*</span>
            </label>
            <input
              type="number"
              id="age"
              name="age"
              value={formData.age}
              onChange={handleChange}
              required
              min="1"
              max="120"
              placeholder="25"
            />
          </div>

          <div className="form-group">
            <label htmlFor="profession">
              Profession <span className="required">*</span>
            </label>
            <input
              type="text"
              id="profession"
              name="profession"
              value={formData.profession}
              onChange={handleChange}
              required
              placeholder="Software Engineer"
            />
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="interests">
            Interests <span className="required">*</span>
            <span className="hint">(comma-separated)</span>
          </label>
          <input
            type="text"
            id="interests"
            name="interests"
            value={formData.interests}
            onChange={handleChange}
            required
            placeholder="Technology, Reading, Travel, Music"
          />
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="education">Education</label>
            <input
              type="text"
              id="education"
              name="education"
              value={formData.education}
              onChange={handleChange}
              placeholder="Bachelor's in Computer Science"
            />
          </div>

          <div className="form-group">
            <label htmlFor="location">Location</label>
            <input
              type="text"
              id="location"
              name="location"
              value={formData.location}
              onChange={handleChange}
              placeholder="Moscow, Russia"
            />
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="bio">Bio / Additional Information</label>
          <textarea
            id="bio"
            name="bio"
            value={formData.bio}
            onChange={handleChange}
            rows="4"
            placeholder="Tell us more about yourself, your goals, or anything else you'd like to share..."
          />
        </div>

        <button 
          type="submit" 
          className="submit-button"
          disabled={isLoading}
        >
          {isLoading ? 'Analyzing...' : 'Generate Article'}
        </button>
      </form>
    </div>
  );
}

