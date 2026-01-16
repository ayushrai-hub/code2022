import json
    
# this is the JSON object
data = {
  "students": [
    {
      "id": "S001",
      "name": "Alice",
      "semesters": [
        {
          "term": "Fall 2023",
          "subjects": [
            { "name": "Math", "credits": 4, "performance": { "assignments": 80, "exams": 70, "attendance": 85 } },
            { "name": "Physics", "credits": 3, "performance": { "assignments": 90, "exams": 60, "attendance": 70 } }
          ]
        }
      ]
    },
    {
      "id": "S002",
      "name": "Bob",
      "semesters": [
        {
          "term": "Fall 2023",
          "subjects": [
            { "name": "Math", "credits": 4, "performance": { "assignments": 85, "exams": 75, "attendance": 90 } },
            { "name": "English", "credits": 2, "performance": { "assignments": 95, "exams": 82, "attendance": 60 } }
          ]
        }
      ]
    }
  ]
}

# This function calculates final grade using weighted average.
# 30% from assignments, 50% from exams, and 20% from attendance.
def calculate_final_grade(performance):
    for metric in ['assignments', 'exams', 'attendance']:
        if metric not in performance:
            raise ValueError(f"Missing {metric} in performance data")
        if not (0 <= performance[metric] <= 100):
            raise ValueError(f"{metric} score must be between 0 and 100")
    return 0.3 * performance['assignments'] + 0.5 * performance['exams'] + 0.2 * performance['attendance']

# It calculates semester GPA and total credits, and it takes list of subjects as input.
# It returns a tuple of (GPA on a 4.0 scale, total credits)
def calculate_gpa(subjects):
    total_weighted_grades = 0
    total_credits = 0
    for subject in subjects:
        final_grade = calculate_final_grade(subject['performance'])
        subject['final_grade'] = final_grade
        total_weighted_grades += final_grade * subject['credits']
        total_credits += subject['credits']
    gpa = (total_weighted_grades / total_credits) / 100 * 4
    return gpa, total_credits

# This function generates and returns the transcript for a student.
# It shows semester GPAs and cumulative GPA with honors if GPA ≥ 3.7.
def generate_transcript(student):
    cumulative_weighted_grades = 0
    cumulative_credits = 0
    transcript =[]
    transcript.append(f"Transcript for {student['name']} (ID: {student['id']})")
    for semester in student['semesters']:
        transcript.append(f"Term: {semester['term']}")
        gpa, credits = calculate_gpa(semester['subjects'])
        cumulative_weighted_grades += sum(subj['final_grade'] * subj['credits'] for subj in semester['subjects'])
        cumulative_credits += credits
        honors = " with Honors" if gpa >= 3.7 else ""
        transcript.append(f"GPA for this semester: {gpa:.2f}{honors}")
        for subject in semester['subjects']:
            transcript.append(f"  {subject['name']}: {subject['final_grade']:.1f} ({subject['credits']} credits)")
    cumulative_gpa = (cumulative_weighted_grades / cumulative_credits) / 100 * 4
    honors = " with Honors" if cumulative_gpa >= 3.7 else ""
    transcript.append(f"Cumulative GPA: {cumulative_gpa:.2f}{honors}\n")
    return "\n".join(transcript)

def process_transcripts(data):
    for student in data['students']:
        print(generate_transcript(student))
        
process_transcripts(data)