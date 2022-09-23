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
  const [courseResult, setCourseResult] = useState({})

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

  }, [])


  // Give suggestions of possible search words based on the input prefix
  // TODO: handle spaces between words
  const getSuggestions = (text) => {
    if (trie === {}) return []
    const limit = 3
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
      Object.keys(node).forEach((child) => {
        if (child === '#') {
          output.push(node['#'])
          if (output.length > limit) return output
        }
        else {
          stack.push(node[child])
        }
      })
    }

    return output
  }

  // User entered some search word
  const handleChange = (e) => {
    let text = e.target.value
    setSearchText(text)

    if (text) {
      console.log(text)
      let suggestedWords = getSuggestions(text)
      //TODO: May be the user only wants to search for a single word. 
      console.log(suggestedWords)
      let coursesIndices = {}
      for (const word of suggestedWords) {
        if (word in index) {
          // console.log(index[word])
          for (const course of Object.keys(index[word])) {
            // console.log(course)
            if (!(course in coursesIndices)) {
              coursesIndices[course] = [[], []]
            }
            coursesIndices[course][0].push(...index[word][course][0])
            coursesIndices[course][1].push(...index[word][course][1])
          }
        }
      }
      setCourseResult(coursesIndices)
    }
  }

  useEffect(() => {
    console.log(courseResult)
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


      {/* <pre>{JSON.stringify(index)}</pre> */}
      <br />

      <Drawer
        open={searchText !== ''}
        anchor={'bottom'}
        variant='persistent'
        keepMounted
        PaperProps={{
          sx: { height: "85%" },
        }}
      // disableAutoFocus
      >

        <Grid2

          container
          spacing={{ xs: 2, md: 3 }}

        >

          {Object.entries(courseResult).map(([courseName, indices]) => (
            <CourseCard />

            
          ))}

        </Grid2>
      </Drawer>
    </>

  )
}

export default Searchbar