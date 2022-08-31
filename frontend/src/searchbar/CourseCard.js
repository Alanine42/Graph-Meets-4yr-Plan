import { Card, CardContent, CardActions, Grid, Button } from '@mui/material'
import Grid2 from '@mui/material/Unstable_Grid2'
import React from 'react'

// Display one course module
// highlight relevant parts
const CourseCard = ({ subject, courseID, name, description, onClick }) => {
  return (
    <Grid2 
    item 
    xs={12} 
    sm={12}
    md={6}
    lg={4}
    xl={3}
    >
      <a onClick={onClick}>
        <Card>
          <CardContent>{courseID + " " + name}</CardContent>
          <CardContent>{description}</CardContent>

          <CardActions>
            <Button size="small">Wanna take</Button>
            
          </CardActions>

        </Card>
      </a>
    </Grid2>
  )
}

export default CourseCard

// button: set/unset wanna take (message bar + undo option)
// link to other courses (prereq, unlocks)