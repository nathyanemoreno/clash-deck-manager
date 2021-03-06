import { makeStyles } from '@material-ui/core';

export default makeStyles(theme => ({
  cardContent: {
    background: '#8F9FDD',
  },
  paper: {
    padding: theme.spacing(2),
    textAlign: 'center',
    // background: '#384A5E',
    // backgroundPositionX: 'center',
    // backgroundPositionY: 'center'
  },
  grid: {
    padding: theme.spacing(2)
  },
  w100: {
    width: '100%'
  },
  h100: {
    height: '100%',
  },
  card: {
    height: 110  
  },
  zone: {
    background: 'rgba(0, 0, 0, 0.4)',
    height: '65px'
  },
  largeZone: {
    background: 'rgba(0, 0, 0, 0.4)',
    height: '220px',
    cursor: 'pointer'
  },
  left: {
    // background: `url(${bg2})`, //'#478AC2',
    overflowY: 'auto'
  },
  deckTitle: {
    fontWeight: 900,
    color: 'rgba(255, 255, 255, 0.9)',
    textShadow: '1px 1px 2px #000',
    marginLeft: theme.spacing(1)
  },
  deckHeader: {
    color: '#fff',
    textShadow: '2px 2px 3px #000',
    marginBottom: theme.spacing(1),
    textAlign: 'left'
  },
  icon: {
    color: 'rgba(255, 255, 255, 0.7)'
  },
  cardHeader: {
    background: '#5963ab',
    padding: theme.spacing(1)
  },
  cardFoot: {
    background: '#5963ab',
    justifyContent: 'space-between'
  },
  wFill: {
    width: `calc(80% - 40px)`
  },
  modal: {
    display: 'flex',
    padding: theme.spacing(1),
    alignItems: 'center',
    justifyContent: 'center',
  },
  paper_modal: {
    width: 600,
    height: 400,
    overflowY: 'auto',
    // backgroundColor: theme.palette.background.paper,
    borderRadius: theme.spacing(1),
    boxShadow: theme.shadows[5],
    padding: theme.spacing(2),
    background: '#384A5E'
  },
  elixirBadge: {
    position: 'absolute',
    width: 30,
    right: -5,
    top: -5
  },
  elixirCusto: {
    position: 'absolute',
    right: 5,
    top: -15,
    color: '#fff',
    textShadow: '2px 2px 3px #000',
    fontWeight: 700
  },
  modalCancelBtn: {
    marginBottom: theme.spacing(2),
    float: 'right'
  },
  modalTitle: {
    float: "left",
    color: '#fff',
    textShadow: '2px 2px 3px #000',
    fontWeight: 700
  }
}))