import React from 'react';
import { Grid, Paper, Typography, IconButton, TextField, CardActions, Card,
CardHeader, CardContent, Input, Modal, Button, Tooltip } from '@material-ui/core';
import DeleteIcon from '@material-ui/icons/Delete';
import EditIcon from '@material-ui/icons/Edit';
import SearchIcon from '@material-ui/icons/Search';
import HelpIcon from '@material-ui/icons/Help';
import useStyle from './classes';
import './App.css';
import api from './services/api';

const Elixir = require('./media/Elixir.png')

const cls = (...item) => item.join(' ')
const parseText = (text) => text.toLowerCase().split('-').join(' ').split('.').join(' ')
const makeImgName = (name) => parseText(name).normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/(?:^|\s)\S/g, e => e.toUpperCase()).split(' ').join('');

function App() {
  const classes = useStyle();
  const [open, setOpen] = React.useState(false);
  const [cards, setCartas] = React.useState([]);
  const [currentDeck, setCurrentDeck] = React.useState({
    cards: Array(8).fill(null)
  });
  const [currentCard, setCurrentCard] = React.useState();
  const [isEditing, setIsEditing] = React.useState(false);
  const [queryText, setQueryText] = React.useState();
  const [lastQueryText, setLastQueryText] = React.useState();
  const [decks, setDecks] = React.useState([]);
  const rootRef = React.useRef(null);

  const handleSearchChange = e => {
    const target = e.target;
    setQueryText(target.value);
  }

  const startSearch = () => {
    // e.preventDefault();
    const last = queryText;
    if (queryText === '') {
      api.get(`/list_decks`).then(res => {
        setDecks(res.data.decks.map((e, i)  => ({...e, index: i, cards: e.cards.map(c => ({...c, img: require(`./media/cards/${makeImgName(c.card_name)}Card.png`)}))})));
      })
    } else {
      api.get(`/find_deck?query=${queryText}`).then(res => {
        setDecks(res.data.decks.map((e, i)  => ({...e, index: i, cards: e.cards.map(c => ({...c, img: require(`./media/cards/${makeImgName(c.card_name)}Card.png`)}))})));
      })
    }
    setLastQueryText(last);
  }
  
  const handleSelect = i => e => {
    e.preventDefault();
    setOpen(true);
    setCurrentCard(i);
  }

  const handleChange = tipo => e => {
    const target = e.target;
    setCurrentDeck(old => ({...old, [tipo]: target.value}));
  }

  const handleCardSelect = card => e => {
    e.preventDefault();
    setOpen(false);
    setCurrentDeck(old => {
      old.cards[currentCard] = card;
      return old;
    })
    setCartas(old => {
      if (currentDeck.cards[currentCard]) {
        return [...old, currentDeck.cards[currentCard]].map(e => e !== card ? e : null)
      } else {
        return old.map(e => e !== card ? e : null)  
      }
    });
  }

  const createDeck = (deckData) => {
    return (
      <Grid item md={6}>
        <Card className={classes.card}>
          <CardHeader
            title={<Typography variant="body1" className={classes.deckTitle}>{`${deckData.name}#${deckData.deck_code}`}</Typography>}
            // subheader={<Typography variant="subtitle2">September 14, 2016</Typography>}
            className={classes.cardHeader}
            action={
              <Tooltip title={
              <div>
                <p>{deckData.description}</p>
                <p>{deckData.created_at}</p>
              </div>}
              style={{marginRight: '10px', marginTop: '10px'}}>
                <HelpIcon className={classes.icon}/>
              </Tooltip>
            }
          />
          <CardContent className={classes.cardContent}>
            <Grid container spacing={2}>
              {deckData.cards.map(card => (
                <Grid item md={3}>
                  <img
                      className={classes.card}
                      src={require(`./media/cards/${makeImgName(card.card_name)}Card.png`)}
                      title={card.card_name}
                      alt={card.card_name}
                    />
                </Grid>
              ))}
            </Grid>
          </CardContent>
          <CardActions disableSpacing className={classes.cardFoot}>
            <div style={{
              display: 'flex',
              alignItems: 'inherit',
              justifyContent: 'inherit'
            }}>
              <IconButton size='small'>
                <img alt='Elixir' src={Elixir} style={{height: '24px'}} />
              </IconButton>
              <Typography className={classes.deckTitle}>
                <strong>{deckData.elixir_cost}</strong>
              </Typography>
            </div>
            <div>
              <IconButton size='small' className={classes.icon} onClick={() => {
                setCurrentDeck({
                  ...deckData,
                  cards: Array(8).fill(null).map((e, i) => deckData.cards[i] ? deckData.cards[i] : null)
                });
                setIsEditing(true);
              }}>
                <EditIcon />
              </IconButton>
              <IconButton size='small' className={classes.icon} onClick={handleDelete(deckData.deck_code, deckData.index)}>
                <DeleteIcon />
              </IconButton>
            </div>
          </CardActions>
        </Card>
      </Grid>
    );
  }

  function saveDeck(e) {
    e.preventDefault();
    setIsEditing(false);
    const cards = currentDeck.cards.filter(v => v !== null).map((e, i) => ({...e, index: i}));
    const elixir_cost = Math.round(10 * cards.map(card => card.card_elixir_cost).reduce((a, b) => a + b,0) / cards.length) / 10;
    const data = new Date().toISOString().substring(0, 10);
    api.post(`/add_deck?description=${currentDeck.description}&name=${currentDeck.name}&elixir_cost=${elixir_cost}&created_at=${data}&cards=${JSON.stringify(cards.map(v => ({card_number: v.card_number, index_card: v.index})))}`)
    .then(v => {
      alert('Deck salvo com Sucesso!')
    })
    .catch(error => {
      console.error(error);
      alert('Não foi possível salvar o Deck!')
    })
  }

  function updateDeck(e) {
    e.preventDefault();
    const cards = currentDeck.cards.filter(v => v !== null).map((e, i) => ({...e, index: i}));
    const elixir_cost = Math.round(10 * cards.map(card => card.card_elixir_cost).reduce((a, b) => a + b,0) / cards.length) / 10;
    api.post(`/update_deck?deck_code=${currentDeck.deck_code}&description=${currentDeck.description}&name=${currentDeck.name}&elixir_cost=${elixir_cost}&cards=${JSON.stringify(cards.map(v => ({...v, index_card: v.index})))}`)
    .then(v => {
      alert('Deck alterado com Sucesso!')
    })
    .catch(error => {
      console.error(error);
      alert('Não foi possível alterar o Deck!')
    })
  }

  const handleDelete = (codigo, index) => (e) => {
    e.preventDefault();
    api.post(`/remove_deck?deck_code=${codigo}`)
    .then(v => {
      startSearch();
      alert('Deck deletado com Sucesso');
    })
    .catch(error => {
      console.error(error);
      alert('Não foi possível deletado o Deck')
    })
  }

  React.useEffect(() => {
    api.get('/list_cards').then(res => {
      const data = res.data;
      console.log(data);
      setCartas(Object.values(data).map(e => ({...e, card_elixir_cost: e.elixir_cost, img: require(`./media/cards/${makeImgName(e.name)}Card.png`)})));
    })
    .catch(error => {
      console.error(error);
      alert('Não foi possível obter as cards.')
    });
  }, []);

  return (
    <div className={classes.h100}>
      <Grid container className={classes.h100}>
        <Grid item lg={6} className={cls(classes.grid, classes.h100)}>
          <Paper className={classes.paper} style={{height: 'calc(100% - 32px)'}}>
            <Typography style={{marginBottom: '16px'}} variant="h4"><strong>Clash Royale Deck Manager</strong></Typography>
            <TextField style={{marginBottom: '16px'}} label="Nome do Deck" variant="outlined" fullWidth inputProps={{ maxLength: 50 }} onChange={handleChange('name')} value={currentDeck.name ? currentDeck.name : ''}/>
            <TextField label="Descrição" variant="outlined" fullWidth inputProps={{ maxLength: 200 }} multiline rowsMax={3} onChange={handleChange('description')} value={currentDeck.description ? currentDeck.description : ''}/>
            <center>  
              <Grid container spacing={2} style={{width: '90%', margin: '20px 0'}}>
                {currentDeck.cards.map((e, i) => (
                  <Grid item md={3}>
                    <Paper className={classes.largeZone} onClick={handleSelect(i)}>
                      {e && (
                        <img
                          className={classes.w100}
                          src={e.img}
                          title={e.name}
                          alt={e.name}
                        />
                      )}
                    </Paper>
                  </Grid>
                ))}
              </Grid>
            </center>
            <div style={{float: 'right'}}>
              {isEditing && <Button variant='outlined' color='primary' onClick={updateDeck}>Atualizar</Button>}
              {' '}
              <Button variant='contained' color='primary' onClick={saveDeck}>Salvar novo</Button>
            </div>
          </Paper>
        </Grid>
        <Grid item lg={6} className={cls(classes.grid, classes.left, classes.h100)}>
          <Paper className={classes.paper} style={{marginBottom: '16px'}}>
            <Grid container spacing={1} alignItems="flex-end">
              <Grid item>
                <SearchIcon />
              </Grid>
              <Grid item className={classes.wFill}>
                <Input placeholder="Pesquisar" fullWidth onChange={handleSearchChange}/>
              </Grid>
              <Grid item>
                <Button variant='contained' color='primary' onClick={startSearch}>Pesquisar</Button>
              </Grid>
            </Grid>
          </Paper>
          <Grid container spacing={2}>
            {decks.map(deck => (
              createDeck(deck)
            ))}
          </Grid>
        </Grid>
      </Grid>

      <Modal
        disablePortal
        disableEnforceFocus
        disableAutoFocus
        open={open}
        className={classes.modal}
        container={() => rootRef.current}
      >
        <div className={classes.paper_modal}>
          <div>
            <Typography className={classes.modalTitle} variant='h5'>Escolha uma card</Typography>
            <Button variant='contained' color='secondary' className={classes.modalCancelBtn} onClick={() => setOpen(false)}>Cancelar</Button>
          </div>
          <Grid container spacing={1}>
            {cards.map((e, i) => (
              e ? (
                <Grid item md={2} key={i}>
                  <div style={{position: 'relative'}}>
                    <img
                      src={e.img}
                      alt={e.name}
                      title={e.name}
                      className={classes.w100}
                      style={{cursor: 'pointer'}}
                      onClick={handleCardSelect(e)}
                    />
                    <img src={Elixir} alt='Elixir' className={classes.elixirBadge} />
                    <p className={classes.elixirCusto}>{e.card_elixir_cost}</p>
                  </div>
                </Grid>
              ) : null
            ))}
          </Grid>
        </div>
      </Modal>
    </div>
  );
}

export default App;
