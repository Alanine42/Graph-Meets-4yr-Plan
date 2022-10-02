import React, { useEffect, useState } from 'react';
import { styled, alpha } from '@mui/material/styles'
import { AppBar, Toolbar, TextField, Grid, IconButton, Typography, Drawer } from "@mui/material"
import Grid2 from '@mui/material/Unstable_Grid2'
import MenuItem from '@mui/material/MenuItem';
import Menu from '@mui/material/Menu';
import MenuIcon from '@mui/icons-material/Menu';
import SearchIcon from '@mui/icons-material/Search';
import InputBase from '@mui/material/InputBase';
import AccountCircle from '@mui/icons-material/AccountCircle';
import MailIcon from '@mui/icons-material/Mail';
import NotificationsIcon from '@mui/icons-material/Notifications';
import MoreIcon from '@mui/icons-material/MoreVert';
import { fakeIndex, fakeCourseResult } from './mockData'
import CourseCard from './CourseCard';
import axios from 'axios'

const Search = styled('div')(({ theme }) => ({
  position: 'relative',
  borderRadius: theme.shape.borderRadius,
  backgroundColor: alpha(theme.palette.common.white, 0.15),
  '&:hover': {
    backgroundColor: alpha(theme.palette.common.white, 0.25),
  },
  marginRight: theme.spacing(2),
  marginLeft: 0,
  width: '100%',
  [theme.breakpoints.up('sm')]: {
    marginLeft: theme.spacing(3),
    width: 'auto',
  },
}));

const SearchIconWrapper = styled('div')(({ theme }) => ({
  padding: theme.spacing(0, 2),
  height: '100%',
  position: 'absolute',
  pointerEvents: 'none',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
}));

const StyledInputBase = styled(InputBase)(({ theme }) => ({
  color: 'inherit',
  '& .MuiInputBase-input': {
    padding: theme.spacing(1, 1, 1, 0),
    // vertical padding + font size from searchIcon
    paddingLeft: `calc(1em + ${theme.spacing(4)})`,
    transition: theme.transitions.create('width'),
    width: '100%',
    [theme.breakpoints.up('xs')]: {
      width: '27ch',
    },
    [theme.breakpoints.up('md')]: {
      width: '55ch',
    },
    [theme.breakpoints.up('lg')]: {
      width: '90ch',
    },
    [theme.breakpoints.up('xl')]: {
      width: '120ch',
    },
  },
}));


const Searchbar = () => {
  const [trie, setTrie] = useState({})
  const [index, setIndex] = useState({})
  const [searchText, setSearchText] = useState('')
  const [courseResult, setCourseResult] = useState([])
  const [cache, setCache] = useState({})
  const [prereqs, setPrereqs] = useState({})

  // Fetch the index from django backend
  // "key word/phrase": ["CSE 21", "Math 154", "CSE 101"]
  useEffect(() => {
    axios.get('http://127.0.0.1:8000/api/trie')
      .then(res => {
        setTrie(res.data)
        // console.log(res.data)
      })

    axios.get('http://127.0.0.1:8000/api/index')
      .then(res => {
        setIndex(res.data)
        // console.log(res.data)
      })

    axios.get('http://127.0.0.1:8000/api/prereqs')
      .then(res => {
        // console.log(res.data)
        setPrereqs(res.data)
      })

  }, [])


  // Helper: Give suggestions of possible search words based on the input prefix
  // TODO: handle spaces between words
  const getSuggestions = (text) => {
    if (trie === {}) return []
    const limit = 15
    let output = []
    let node = trie
    for (const char of text.toLowerCase()) {
      if (!node.hasOwnProperty(char)) {
        return output
      }
      node = node[char]
    }

    let stack = [node]
    while (stack.length) {
      let node = stack.pop()
      for (const child of Object.keys(node)) {
        if (child === '#') {
          output.push(node['#'])
          if (output.length > limit) return output
        }
        else {
          stack.push(node[child])
        }
      }
    }

    return output
  }

  // Helper: Highlight words at specific indices
  // TODO [!]: BUG. Algorithm part. Probably slice() , checking nextD ending condition. 
  const highlightWordsAtIndices = (text, indices) => {
    if (indices.length === 0) return text

    let output = []
    let prev = 0

    for (let i of indices) {
      output.push(text.slice(prev, i))
      let nextD = i
      while (nextD < text.length && !(text[nextD]==' ' || text[nextD]==',' ||text[nextD]=='.')) {
        nextD++
      }
      // console.log(text.slice(i, nextD))
      output.push("<mark>" + text.slice(i, nextD) + "</mark>")
      prev = nextD
    }
    output.push(text.slice(prev))

    console.log(output)
    return output.join('')
  }

  // User entered some search word
  let timerID = null
  const handleChange = (e) => {
    if (timerID !== null) {
      clearTimeout(timerID)
    }

    timerID = setTimeout(handleSearch, 100, e.target.value)
  }

  const handleSearch = (text) => {
    setSearchText(text)

    if (text) {
      console.log(text)
      let suggestedWords = getSuggestions(text)
      // console.log(suggestedWords)
      // Get courses (that have suggestedWords) from index
      let coursesIndices = {}
      let count = 0
      for (const word of suggestedWords) {
        if (word in index) {
          // console.log(index[word])
          for (const course of Object.keys(index[word])) {
            // console.log(course)
            if (!(course in coursesIndices)) {
              if (count > 40) continue
              coursesIndices[course] = [[], [], '', ''] // [indices of words in title, indices of words in description, course title, course description]
              count += 1

            }
            coursesIndices[course][0].push(...index[word][course][0])
            coursesIndices[course][1].push(...index[word][course][1])
          }
        }
      }

      // console.log(coursesIndices)

      // 1. Fetch the course description from django backend OR local cache
      for (const course of Object.keys(coursesIndices)) {
        if (course in cache) {
          coursesIndices[course][2] = cache[course][0]
          coursesIndices[course][3] = cache[course][1]
        }
        else {
          axios.get('http://127.0.0.1:8000/api/courseDetail/' + course.replace(' ', '_'))
            .then(res => {
              // console.log(res.data)
              coursesIndices[course][2] = res.data.name
              coursesIndices[course][3] = res.data.description
              setCache({ ...cache, [course]: [res.data.title, res.data.description] })
            })
        }
      }


      // console.log(cache)

      // 2. Sort the courses based on the number of words matched
      let result = Object.entries(coursesIndices).sort((x, y) => {
        let x1 = x[1][0].length + x[1][1].length
        let y1 = y[1][0].length + y[1][1].length
        return y1 - x1
      })
      console.log(result)

      // 3. Wrap words-to-highlight in the course name and description with <mark> tag
      let resultWithMark = result.map((course) => {
        const name = course[1][2]
        const description = course[1][3]
        const indicesName = course[1][0]
        const indicesDescription = course[1][1]

        let nameWithMark = highlightWordsAtIndices(name, indicesName)
        let descriptionWithMark = highlightWordsAtIndices(description, indicesDescription)

        return [nameWithMark, descriptionWithMark]
      })

      setCourseResult(resultWithMark)
    }

  }

  // Update course cards displayed with search words highlighted. 
  useEffect(() => {
    // console.log(courseResult)



  }, [courseResult])


  // only when the search bar has text in it, will it display the search page.
  // Other times, the page displays graph data structure

  return (
    <>
      <AppBar position="fixed">
        <Toolbar>
          <IconButton size="large" edge="start" color="inherit" aria-label="open drawer" sx={{ mr: 2 }}>
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div" sx={{ display: { xs: 'none', sm: 'block' } }}>
            Captain Catalog
          </Typography>

          <Search>
            <SearchIconWrapper>
              <SearchIcon />
            </SearchIconWrapper>
            <StyledInputBase
              placeholder="Search…"
              inputProps={{ 'aria-label': 'search', 'autoFocus': 'true' }}
              onChange={handleChange}
            />
          </Search>
        </Toolbar>
      </AppBar>

      <Drawer
        open={searchText !== ''}
        anchor={'bottom'}
        variant='persistent'
        keepMounted
        PaperProps={{
          sx: { height: "85%" },
        }}
      >

        <Grid2
          container
          spacing={{ xs: 2, md: 3 }}
        >

          {courseResult.map(([name, description]) => (
            <CourseCard cName={name} cDescription={description} />

          ))}

        </Grid2>
      </Drawer>
    </>

  )
}

export default Searchbar